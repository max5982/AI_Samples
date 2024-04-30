import PyPDF2

pdf_file = "model_s_owners_manual_na_english_5.9.pdf"

# Load & Extract
with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

# Save
with open('extracted_ppypdf2.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(text)
