
# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy client application
COPY app/client.py .

# Create client data directory
RUN mkdir -p /clientdata

# Start client application
CMD ["python", "-u", "client.py"]
