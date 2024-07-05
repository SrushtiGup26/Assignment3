# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory to /app in the container
COPY . /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install additional dependencies if needed (e.g., for SQL Server)
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++

# Set environment variables
ENV SQL_SERVER_HOST=<your_sql_server_host>
ENV SQL_SERVER_DATABASE=<your_sql_server_database>

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "FinalCode.py"]
