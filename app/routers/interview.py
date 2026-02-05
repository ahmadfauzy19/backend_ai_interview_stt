"""
Interview Router
Endpoints untuk transcription dan audio processing
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime

from app.services.whisper_services import (
    transcribe_audio
)
from app.utils.file_utils import save_temp_file, cleanup_file
from app.schemas import TranscriptionResponse, TranscriptionWithTimestampsResponse

router = APIRouter(prefix="/media", tags=["Media"])


# =========================
# Transcribe (Plain Text)
# =========================

@router.post(
    "/transcribe",
    response_model=TranscriptionResponse,
    summary="Transkripsi Audio ke Text",
    description="Transkripsi file audio menggunakan Faster Whisper",
    responses={
        200: {"description": "Transcription successful"},
        400: {"description": "Invalid request"},
        404: {"description": "File not found"},
    }
)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """
    Transcribe audio file to plain text
    
    - **file**: Audio file to transcribe (required)
    
    Returns transcribed text without timestamps.
    """
    temp_path = None
    try:
        temp_path = save_temp_file(file)
        text = transcribe_audio(temp_path, language="id")

        return TranscriptionResponse(
            message="Transkripsi success",
            text=text,
            timestamp=datetime.now(),
        )

    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(400, f"Error dalam transkripsi: {str(e)}")
    finally:
        cleanup_file(temp_path)