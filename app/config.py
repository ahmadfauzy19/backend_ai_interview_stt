"""
Application Configuration
Centralized configuration for the entire application
"""

import os
from typing import Dict, Any

# ========================
# Environment Settings
# ========================
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ========================
# CORS Settings
# ========================
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8081",
]

CORS_CONFIG = {
    "allow_origins": CORS_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# ========================
# API Settings
# ========================
API_TITLE = "AI Interview API"
API_DESCRIPTION = "Backend API untuk AI Interview Recording dan Processing"
API_VERSION = "1.0.0"

# ========================
# File Storage Settings
# ========================
UPLOAD_DIR = "app/storages/tmp"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# ========================
# Whisper Model Settings
# ========================
WHISPER_MODEL_NAME = "cahya/faster-whisper-medium-id"

WHISPER_MODEL_CONFIG: Dict[str, Any] = {
    "device": "cpu",
    "compute_type": "int8",
    "cpu_threads": 8,
}

WHISPER_TRANSCRIBE_CONFIG: Dict[str, Any] = {
    "beam_size": 5,
    "condition_on_previous_text": False,
}

# Default language for transcription
DEFAULT_LANGUAGE = "id"

# ========================
# Logging Settings
# ========================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
