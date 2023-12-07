# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install any needed packages specified in requirements.txt and update the errors
#RUN pip install --upgrade Flask Werkzeug

# Expose port 5000 to the outside world
EXPOSE 5000

# Run gunicorn to serve the application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
