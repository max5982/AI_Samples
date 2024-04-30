import PyPDF2
import re

pdf_file = "model_s_owners_manual_na_english_5.9.pdf"

# Load & Extract
with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

# Clean
#clean_text = re.sub(r'\s+', ' ', text)
#clean_text = re.sub(r'\s+', ' ', text).strip()
#clean_text = re.sub(r'Page \d+ of \d+|\n.*:', '', text)
#clean_text = re.sub(r'https?://\S+|www\.\S+|\S+@\S+', '', text)
#clean_text = text.lower()
clean_text = re.sub(r'(?<![\.\:\?\!])\n', ' ', text).strip()


# Save
with open('extracted_ppypdf2_clean.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(clean_text)
