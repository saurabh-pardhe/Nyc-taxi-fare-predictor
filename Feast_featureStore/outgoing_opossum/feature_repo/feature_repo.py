from feast import Entity, FeatureView, Field, BigQuerySource, FeatureStore
from feast.types import Int64, Float32, String
from feast.value_type import ValueType
from datetime import timedelta

# 1) Define the Entity object
trip = Entity(
    name="trip_id",
    value_type=ValueType.STRING,
    description="Unique UUID for each taxi trip"
)

# 2) Point to your BQ table
bq_source = BigQuerySource(
    table="opportune-baton-464110-c1.VLBA.Taxi_data_features_split",
    timestamp_field="pickup_ts",
    created_timestamp_column="created_ts",
)

# 3) FeatureView must refer to the Entity, not its name
taxi_fv = FeatureView(
    name="taxi_features",
    entities=[trip],
    ttl=timedelta(days=1),
    source=bq_source,
    schema=[
        Field(name="pickup_bin",       dtype=Int64),
        Field(name="dropoff_bin",      dtype=Int64),
        Field(name="trip_time_s",      dtype=Int64),
        Field(name="passenger_count",  dtype=Int64),
        Field(name="trip_distance",    dtype=Float32),
        Field(name="RatecodeID",       dtype=Int64),
        Field(name="PULocationID",     dtype=Int64),
        Field(name="DOLocationID",     dtype=Int64),
        Field(name="total_surcharges", dtype=Float32),
        Field(name="airport_fee",      dtype=Float32),
        Field(name="total_amount",     dtype=Float32),
        Field(name="split",            dtype=String),
    ],
    online=False,
)

if __name__ == "__main__":
    fs = FeatureStore(repo_path=".")
    fs.apply([trip, taxi_fv])