FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Install base packages first
RUN pip install --no-cache-dir --timeout=600 --retries=5 -r requirements.txt

# Install the large Azure package separately with extended timeout and more retries
RUN pip install --no-cache-dir --timeout=1200 --retries=15 azure-cognitiveservices-speech

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
