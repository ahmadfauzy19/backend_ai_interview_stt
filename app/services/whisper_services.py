"""
Whisper Transcription Services
Main transcription functions
"""

import time
from typing import List, Dict
from app.services.model_manager import get_whisper_model
from app.config import WHISPER_TRANSCRIBE_CONFIG, DEFAULT_LANGUAGE
from app.logger import setup_logger
from app.utils.file_utils import validate_file_exists

logger = setup_logger(__name__)


def transcribe_audio(audio_file_path: str, language: str = DEFAULT_LANGUAGE) -> str:
    """
    Transcribe audio file to plain text
    
    Args:
        audio_file_path: Path to audio file
        language: Language code (default: "id")
        
    Returns:
        str: Transcribed text
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
    validate_file_exists(audio_file_path)

    logger.info(f" Start transcribing: {audio_file_path}")
    start_time = time.time()

    model = get_whisper_model()
    segments, info = model.transcribe(
        audio_file_path,
        language=language,
        **WHISPER_TRANSCRIBE_CONFIG,
    )

    lines = []
    for seg in segments:
        # Filter silence dari model (kalau tersedia)
        if hasattr(seg, "no_speech_prob") and seg.no_speech_prob > 0.6:
            continue

        # Filter confidence rendah (optional tapi bagus)
        if hasattr(seg, "avg_logprob") and seg.avg_logprob < -1.0:
            continue
        line = seg.text.strip()
        if line:
            lines.append(line)

    result = "\n".join(lines).strip()

    elapsed_time = time.time() - start_time
    logger.info(
        f"📝 Transcription finished | segments={len(lines)} | time={elapsed_time:.2f}s"
    )
    if not result or len(result) < 3:
        logger.info("No valid speech detected → return '...'")
        return "..."

    return result