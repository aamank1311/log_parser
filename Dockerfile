# Use official Python image from Docker Hub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir requirements.txt

# Expose the port on which your Flask app runs
EXPOSE 8080

# Command to run the Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "-t", "60", "app:app"]

