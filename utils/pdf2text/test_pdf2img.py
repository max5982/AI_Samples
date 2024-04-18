from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def pdf_to_text_ocr(filename):
    # Convert PDF to a list of images
    images = convert_from_path(filename)
    
    text = ""
    for image in images:
        # Use Tesseract to do OCR on the converted PDF
        text += pytesseract.image_to_string(image)

    with open('output_ocr.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("PDF text extracted to output_text_ocr.txt")

# Example usage
pdf_to_text_ocr('tesla-owner-manual.pdf')

