# Use the official Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variable for HOME directory
ENV HOME=/app

# Set the working directory to the HOME directory
WORKDIR $HOME

# Copy the requirements file into the container at HOME directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main.py file into the container at HOME directory
COPY main.py .

# Set the default command to execute when the container starts
CMD ["python", "main.py"]
