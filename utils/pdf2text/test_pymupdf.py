import fitz  # PyMuPDF

def pdf_to_text_fitz(filename):
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()

    with open('output_fitz.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("PDF text extracted to output_text_fitz.txt")

# Example usage
pdf_to_text_fitz('tesla-owner-manual.pdf')

