from faster_whisper import WhisperModel
import os
import time
import logging
from typing import List, Dict

# =========================
# Logger setup
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =========================
# Model Config
# =========================

MODEL_NAME = "cahya/faster-whisper-medium-id"

MODEL_CONFIG = {
    "device": "cpu",
    "compute_type": "int8",
}

TRANSCRIBE_CONFIG = {
    "beam_size": 5,
    "condition_on_previous_text": False,
}

# =========================
# Load model once
# =========================

logger.info("🚀 Loading Whisper model...")
start_load = time.time()

model = WhisperModel(MODEL_NAME, **MODEL_CONFIG)

logger.info(
    "✅ Whisper model loaded in %.2f seconds",
    time.time() - start_load
)

# =========================
# Helpers
# =========================

def _validate_file(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

# =========================
# Transcribe plain text
# =========================

def transcribe_audio(audio_file_path: str, language: str = "id") -> str:
    """
    Transkripsi audio ke teks dengan timestamp inline
    """
    _validate_file(audio_file_path)

    logger.info("🎧 Start transcribing: %s", audio_file_path)
    start_time = time.time()

    segments, info = model.transcribe(
        audio_file_path,
        language=language,
        **TRANSCRIBE_CONFIG,
    )

    lines = []
    count = 0
    for seg in segments:
        count += 1
        lines.append(
            f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text.strip()}"
        )
        print(lines[count-1])

    logger.info(
        "📝 Transcription finished | segments=%d | time=%.2fs",
        count,
        time.time() - start_time
    )

    return "\n".join(lines)

# =========================
# Transcribe with timestamps
# =========================

def transcribe_audio_with_timestamps(
    audio_file_path: str,
    language: str = "id"
) -> List[Dict]:
    """
    Transkripsi audio dan kembalikan list segment dengan timestamp
    """
    _validate_file(audio_file_path)

    logger.info("🎧 Start transcribing (timestamps): %s", audio_file_path)
    start_time = time.time()

    segments, info = model.transcribe(
        audio_file_path,
        language=language,
        **TRANSCRIBE_CONFIG,
    )

    results = []
    count = 0
    for seg in segments:
        count += 1
        results.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
        })

    logger.info(
        "📝 Transcription finished | segments=%d | time=%.2fs",
        count,
        time.time() - start_time
    )

    return results
