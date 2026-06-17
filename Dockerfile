# Use an official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# AWS credentials passed as environment variables at runtime
ENV AWS_DEFAULT_REGION=ap-south-1

# Run the fraud detection app
CMD ["python", "app.py"]
