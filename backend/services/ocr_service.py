import pytesseract
from PIL import Image
import PyPDF2
from pathlib import Path
import io

# Configura il percorso di Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path: Path) -> str:
    """Estrae testo da un'immagine usando Tesseract OCR"""
    try:
        image = Image.open(image_path)
        # Usa italiano e inglese per il riconoscimento
        text = pytesseract.image_to_string(image, lang='ita+eng')
        return text.strip()
    except Exception as e:
        raise Exception(f"Errore nell'estrazione testo da immagine: {str(e)}")

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Estrae testo da un PDF"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Errore nell'estrazione testo da PDF: {str(e)}")

def extract_text(file_path: Path, content_type: str) -> str:
    """Determina il tipo di file ed estrae il testo"""
    if content_type == "application/pdf":
        return extract_text_from_pdf(file_path)
    elif content_type in ["image/jpeg", "image/png", "image/jpg"]:
        return extract_text_from_image(file_path)
    else:
        raise Exception(f"Tipo file non supportato: {content_type}")