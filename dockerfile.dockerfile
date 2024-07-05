# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
COPY requirements.txt requirements.txt

# Copy the code from your specified path into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install additional dependencies if needed (e.g., for SQL Server)
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++

# Set environment variables
ENV SQL_SERVER_HOST=DESKTOP-J64M37M\\SQLEXPRESS
ENV SQL_SERVER_DATABASE=Assignment3_AI_in_Enterprise

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "FinalCode.py"]
