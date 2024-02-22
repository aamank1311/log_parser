# Use official Python image from Docker Hub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir Flask==2.1.3 Werkzeug==2.0.2 gunicorn==20.1.0
# Expose the port on which your Flask app runs
EXPOSE 8080

# Command to run the Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]

