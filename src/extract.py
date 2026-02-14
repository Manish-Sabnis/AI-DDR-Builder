import pdfplumber
import re


def extract_inspection_data(pdf_path):
    issues = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Extract impacted area observations from summary table
    pattern = r"Observed (.*?) of (.*?) of Flat No\. 103"
    matches = re.findall(pattern, full_text)

    for match in matches:
        issues.append({
            "issue": match[0].strip(),
            "location": match[1].strip()
        })

    return issues


def extract_thermal_data(pdf_path):
    thermal_entries = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            hotspot = re.search(r"Hotspot\s*:\s*([\d\.]+)", text)
            coldspot = re.search(r"Coldspot\s*:\s*([\d\.]+)", text)

            if hotspot and coldspot:
                thermal_entries.append({
                    "page": i + 1,
                    "hotspot": float(hotspot.group(1)),
                    "coldspot": float(coldspot.group(1))
                })

    return thermal_entries
