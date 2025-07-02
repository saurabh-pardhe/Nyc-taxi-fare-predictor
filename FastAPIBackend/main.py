from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os
from fastapi import File, UploadFile
import io
import joblib

app = FastAPI()
# Used a Nomintim library to get the distance between the locations.
geolocator = Nominatim(user_agent="my_distance_app")
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionInput(BaseModel):
    pickup_bin: int
    dropoff_bin: int
    trip_time_s: int
    passenger_count: int
    trip_distance: float
    RatecodeID: int
    PULocationID: int
    DOLocationID: int
    total_surcharges: float
    airport_fee: float


class InputData(BaseModel):
    pickupLocationId: int
    DroplocationId: int
    numOfPassengers: int
    pickupLocationName: str
    dropLocationName: str


# Load ML model
model = joblib.load("model.pkl")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is up and running"}

# this is a API endpoint that can tke CSV as a i/p and predict the result and o/p, this is useful for stakeholders and output
#can be taken to any application.


@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    try:

        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are accepted")

        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        required_columns = [
            "pickup_bin", "dropoff_bin", "trip_time_s", "passenger_count",
            "trip_distance", "RatecodeID", "PULocationID", "DOLocationID",
            "total_surcharges", "airport_fee"
        ]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV must contain these columns: {required_columns}")

        predictions = model.predict(df)
        return {"predictions": predictions.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(input_data: InputData):
    try:
        pickUpLocation = geolocator.geocode(input_data.pickupLocationName)
        dropLocation = geolocator.geocode(input_data.dropLocationName)

        if not pickUpLocation or not dropLocation:
            raise HTTPException(status_code=404, detail="Location not found")

        point1 = (pickUpLocation.latitude, pickUpLocation.longitude)
        point2 = (dropLocation.latitude, dropLocation.longitude)
        distance = geodesic(point1, point2).miles
        # Assumed few data here , there values can also be taken at random.
        full_data = {
            "pickup_bin": 1,
            "dropoff_bin": 1,
            "trip_time_s": 50,
            "passenger_count": input_data.numOfPassengers,
            "trip_distance": distance,
            "RatecodeID": 2,
            "PULocationID": input_data.pickupLocationId,
            "DOLocationID": input_data.DroplocationId,
            "total_surcharges": 0,
            "airport_fee": 0,
        }

        prediction_input = PredictionInput(**full_data)
        df = pd.DataFrame([prediction_input.model_dump()])
        prediction = model.predict(df)

        return {"prediction": prediction.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))