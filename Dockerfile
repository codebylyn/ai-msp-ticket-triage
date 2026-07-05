FROM python:3.11-slim

WORKDIR /app

# Copy dependencies list and install them inside the container environment only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY triage.py .

# Command to run the application
CMD ["python", "triage.py"]
