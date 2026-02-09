"""
Whisper Model Management
Initialize and manage Whisper model lifecycle
"""

import os
import time
from faster_whisper import WhisperModel
from app.config import WHISPER_MODEL_NAME, WHISPER_MODEL_CONFIG
from app.logger import setup_logger

logger = setup_logger(__name__)

# Force CPU (NO CUDA)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class WhisperModelManager:
    """Singleton manager for Whisper model"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize model if not already loaded"""
        if self._model is None:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load Whisper model"""
        logger.info("Loading Whisper model (CPU int8)...")
        start_load = time.time()
        
        self._model = WhisperModel(WHISPER_MODEL_NAME, **WHISPER_MODEL_CONFIG)
        
        load_time = time.time() - start_load
        logger.info(f"✅ Whisper model loaded in {load_time:.2f} seconds")
    
    @property
    def model(self) -> WhisperModel:
        """Get the loaded model"""
        if self._model is None:
            self._load_model()
        return self._model


# Create global instance
whisper_manager = WhisperModelManager()


def get_whisper_model() -> WhisperModel:
    """Get Whisper model instance"""
    return whisper_manager.model
