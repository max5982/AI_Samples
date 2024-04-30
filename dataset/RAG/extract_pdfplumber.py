import pdfplumber

pdf_file = "model_s_owners_manual_na_english_5.9.pdf"

# Load & Extract
with pdfplumber.open(pdf_file) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() if page.extract_text() else ''

# Save
with open('extracted_pdfplumber.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(text)
