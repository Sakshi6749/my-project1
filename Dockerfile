# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirement.txt .
RUN pip install -r requirement.txt

# Copy the whole application into the container
COPY . .

# Expose the application on port 8000
EXPOSE 8000

# Start the Flask application
CMD ["python", "mainfile.py"]
