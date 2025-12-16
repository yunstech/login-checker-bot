# Use official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    apt-get clean

# Install Playwright dependencies and browsers
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps chromium

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if needed (uncomment if running a web server)
# EXPOSE 8000

# Default command (change main.py if needed)
CMD ["python", "main.py"]
