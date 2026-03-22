# ingestion/parser.py
import re
from PyPDF2 import PdfReader

def extract_assumptions(text):
    sentences = re.split(r'\.|\n', text)
    assumptions = [s.strip() for s in sentences if 'assume' in s.lower() or 'hypothesize' in s.lower()]
    return assumptions

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text
