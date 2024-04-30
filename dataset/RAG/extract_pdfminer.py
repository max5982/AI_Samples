from pdfminer.high_level import extract_text

pdf_file = "model_s_owners_manual_na_english_5.9.pdf"

# Load & Extract
with open(pdf_file, 'rb') as file:
    text = extract_text(file)

# Save
with open('extracted_pdfminer.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(text)
