# Docker configuration will be finalized after the API/dashboard are implemented.
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-c", "print('Phase 1 project initialized')"]
