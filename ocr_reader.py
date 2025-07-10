import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF

def extract_text_from_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def extract_text_from_pdf(pdf_bytes):
    text = ""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text
  
