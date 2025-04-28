import pdfplumber
import docx
from fastapi import UploadFile

def extract_text_from_file(file: UploadFile) -> str:
    content_type = file.content_type

    if content_type == "application/pdf":
        return extract_text_from_pdf(file.file)
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file.file)
    else:
        raise ValueError("Unsupported file type")

def extract_text_from_pdf(file_obj):
    with pdfplumber.open(file_obj) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def extract_text_from_docx(file_obj):
    doc = docx.Document(file_obj)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
