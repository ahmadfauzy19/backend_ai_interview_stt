"""
File Utilities
Helper functions for file operations
"""

import os
import shutil
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import UPLOAD_DIR


def ensure_upload_dir() -> None:
    """Create upload directory if it doesn't exist"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_temp_file(file: UploadFile) -> str:
    """
    Save uploaded file to temporary storage
    
    Args:
        file: UploadFile from FastAPI
        
    Returns:
        str: Path to the saved file
        
    Raises:
        HTTPException: If filename is invalid
    """
    if not file.filename:
        raise HTTPException(400, "Filename tidak valid")

    ensure_upload_dir()

    # Generate unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return path


def cleanup_file(path: Optional[str]) -> None:
    """
    Delete file from storage
    
    Args:
        path: Path to file to delete
    """
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError as e:
            # Log but don't raise - cleanup failure shouldn't crash the app
            print(f"Warning: Could not delete file {path}: {e}")


def validate_file_exists(path: str) -> None:
    """
    Validate that file exists
    
    Args:
        path: Path to file
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
