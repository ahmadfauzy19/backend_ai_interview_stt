FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 PRE-DOWNLOAD WHISPER MODEL (IMPORTANT)
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('base', compute_type='int8')"

# Copy application code
COPY app ./app

RUN mkdir -p /app/app/storages/tmp

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
