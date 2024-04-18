import pdfplumber

def pdf_to_text(filename):
    text = ''
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    with open('output_pdfplumber.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("PDF text extracted to output_text.txt")

pdf_to_text('tesla-owner-manual.pdf')

