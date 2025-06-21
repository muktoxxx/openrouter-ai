# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Pillow with all optional dependencies
RUN pip install --no-cache-dir "Pillow[all]"

# Copy the rest of the application
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the bot
CMD ["python", "src/bot.py"]
