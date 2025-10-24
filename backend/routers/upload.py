from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Verifica tipo file
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo file non supportato")
    
    # Genera nome file unico
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / new_filename
    
    # Salva il file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": new_filename,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "size": file_path.stat().st_size,
        "upload_time": timestamp
    }