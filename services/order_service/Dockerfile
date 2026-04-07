# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose app + metrics ports
EXPOSE 5000 9101

# Run app
CMD ["python", "app.py"]