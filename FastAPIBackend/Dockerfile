# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --upgrade pip

# Set workdir
WORKDIR /app

# Copy your code
COPY . .

# Install Python requirements
RUN pip install -r requirements.txt

# Expose the port used by uvicorn
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]