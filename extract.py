import fitz
import pytesseract
from PIL import Image
import io

# Point to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    total_pages = len(doc)
    
    for i, page in enumerate(doc):
        print(f"Processing page {i+1}/{total_pages}...")
        
        # Convert page to image
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        
        # OCR the image
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    
    return full_text

text = extract_text_ocr(r"e:\Semester8\AI\Lab\Project\bup-guardian\greenbook.pdf")

print("Total characters:", len(text))
print("Preview:", text[:500])

# Save to file so we don't have to OCR again
with open(r"e:\Semester8\AI\Lab\Project\bup-guardian\extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Text saved to extracted_text.txt")