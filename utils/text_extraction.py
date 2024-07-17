# You may need libraries such as PyPDF2 for PDFs, python-docx for docx, etc.
import os
import re
import os
import magic
from PyPDF2 import PdfReader
import docx2txt
import pytesseract
from PIL import Image
import json
import PyPDF2
import docx

# Function to detect file format using magic
def detect_file_format(file_stream):
    mime = magic.Magic(mime=True)
    return mime.from_file(file_stream)


# Function to parse the file contents based on its type
def parse_file_contents(file_stream):
    file_mime_type = detect_file_format(file_stream)
    content = ""

    if 'image' in file_mime_type:
        content = pytesseract.image_to_string(Image.open(file_stream))
    elif 'pdf' in file_mime_type:
        reader = PdfReader(file_stream)
        content = ' '.join(page.extract_text() for page in reader.pages if page.extract_text())
    elif 'wordprocessingml.document' in file_mime_type:  # for DOCX files
        content = docx2txt.process(file_stream)
    elif 'text/plain' in file_mime_type:  # for TXT files
        with open(file_stream, encoding="utf8", errors='ignore') as f:
            content = f.read()
    #elif 'msword' in file_mime_type or file_mime_type.endswith('.doc'):  # for DOC files
    #    content = textract.process(file_path).decode('utf-8')
    else:
        return json.dumps({"error": "Unsupported file type"})
    # If content is empty or not set properly, raise an error
    if not content:
        raise ValueError("Content extraction failed")

    return json.dumps({"content": content}, indent=4)


def extract_text_from_cv(file_stream):
    # Assuming the uploaded file is a PDF
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise e  # Re-raise the exception to be caught by the calling function

def extract_job_description_from_link(link):
    # Placeholder for extracting job description from a link
    # You would use requests, BeautifulSoup, etc. to scrape content from the link
    # Be sure to handle exceptions and errors.
    pass