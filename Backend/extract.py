import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import numpy as np
import cv2

def extract_text(file_stream):
    text = ""
    try:
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        file_stream.seek(0)
        images = convert_from_bytes(file_stream.read())
        for image in images:
            img = np.array(image)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            text += pytesseract.image_to_string(thresh) + "\n"
    return text
