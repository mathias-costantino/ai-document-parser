from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from datetime import datetime
import sys

# Aggiungi la cartella parent al path per importare services
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.ocr_service import extract_text

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
    
    # Estrai il testo con OCR
    try:
        extracted_text = extract_text(file_path, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore OCR: {str(e)}")
    
    return {
        "filename": new_filename,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "size": file_path.stat().st_size,
        "upload_time": timestamp,
        "extracted_text": extracted_text,
        "text_length": len(extracted_text)
    }