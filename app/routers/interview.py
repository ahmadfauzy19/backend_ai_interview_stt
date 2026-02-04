from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import os, shutil, uuid

from app.services.whisper_services import (
    transcribe_audio,
    transcribe_audio_with_timestamps,
)

router = APIRouter(prefix="/media", tags=["Media"])

UPLOAD_DIR = "app/storages/tmp"


# =========================
# Helpers
# =========================

def _save_temp_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(400, "Filename tidak valid")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path


def _cleanup(path: str):
    if path and os.path.exists(path):
        os.remove(path)


# =========================
# Upload Video
# =========================

@router.post(
    "/upload",
    summary="Upload Video Interview",
    description="Upload file video webm dari interview recorder",
)
async def upload_video(file: UploadFile = File(...)):
    if file.content_type != "video/webm":
        raise HTTPException(400, "Invalid file type. Only video/webm allowed")

    video_path = None
    try:
        video_path = _save_temp_file(file)

        return {
            "message": "Upload success",
            "filename": os.path.basename(video_path),
            "file_path": video_path,
            "timestamp": datetime.now().isoformat(),
        }

    finally:
        _cleanup(video_path)


# =========================
# Transcribe (Plain Text)
# =========================

@router.post(
    "/transcribe",
    summary="Transkripsi Audio ke Text",
    description="Transkripsi file audio menggunakan Faster Whisper",
)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    temp_path = None
    try:
        temp_path = _save_temp_file(file)

        text = transcribe_audio(temp_path, language="id")

        return {
            "message": "Transkripsi success",
            "text": text,
            "timestamp": datetime.now().isoformat(),
        }

    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(400, f"Error dalam transkripsi: {str(e)}")
    finally:
        _cleanup(temp_path)


# =========================
# Transcribe with timestamps
# =========================

@router.post(
    "/transcribe-with-timestamps",
    summary="Transkripsi Audio dengan Timestamp",
    description="Transkripsi audio dan kembalikan segment dengan timestamp",
)
async def transcribe_audio_with_timestamps_endpoint(file: UploadFile = File(...)):
    temp_path = None
    try:
        temp_path = _save_temp_file(file)

        segments = transcribe_audio_with_timestamps(temp_path, language="id")

        return {
            "message": "Transkripsi success",
            "segments": segments,
            "total_segments": len(segments),
            "timestamp": datetime.now().isoformat(),
        }

    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(400, f"Error dalam transkripsi: {str(e)}")
    finally:
        _cleanup(temp_path)
