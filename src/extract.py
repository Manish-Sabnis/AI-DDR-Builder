import pdfplumber
import re
import pytesseract
from pdf2image import convert_from_path
import re

def extract_inspection_data(pdf_path):
    issues = []

    with pdfplumber.open(pdf_path) as pdf:
        summary_text = ""

        for page in pdf.pages:
            text = page.extract_text()
            if text and "SUMMARY TABLE" in text:
                summary_text = text
                break

    if not summary_text:
        return []


    summary_text = summary_text.replace("\n", " ")


    pattern = r"Observed (.*?) of Flat No\. 103"
    matches = re.findall(pattern, summary_text)

    for match in matches:
        clean_issue = match.strip()
        if "Flat No. 203" in clean_issue:
            continue

        issues.append({
            "issue": clean_issue
        })

    return issues




def extract_thermal_data(pdf_path):
    thermal_entries = []

    pages = convert_from_path(pdf_path)

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)

        hotspot_match = re.search(r"Hotspot\s*:\s*([\d\.]+)", text)
        coldspot_match = re.search(r"Coldspot\s*:\s*([\d\.]+)", text)

        if hotspot_match and coldspot_match:
            thermal_entries.append({
                "page": i + 1,
                "hotspot": float(hotspot_match.group(1)),
                "coldspot": float(coldspot_match.group(1))
            })

    return thermal_entries




