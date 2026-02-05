"""
Response Schemas
Pydantic models for API responses
"""

from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class TranscriptionSegment(BaseModel):
    """Single transcription segment with timestamp"""
    start: float
    end: float
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "start": 0.0,
                "end": 5.2,
                "text": "Halo, nama saya adalah AI"
            }
        }


class TranscriptionResponse(BaseModel):
    """Response for plain text transcription"""
    message: str
    text: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Transkripsi success",
                "text": "Halo, nama saya adalah AI",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class TranscriptionWithTimestampsResponse(BaseModel):
    """Response for transcription with timestamps"""
    message: str
    segments: List[TranscriptionSegment]
    total_segments: int
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Transkripsi success",
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.2,
                        "text": "Halo, nama saya adalah AI"
                    }
                ],
                "total_segments": 1,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error dalam transkripsi: File tidak valid"
            }
        }
