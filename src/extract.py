import pdfplumber
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

    pattern = r"Observed (.*?) of (.*?) of Flat No\. 103"
    matches = re.findall(pattern, summary_text)

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

            words = page.extract_words()
            if not words:
                continue

            page_text = " ".join(word["text"] for word in words)

            hotspot_match = re.search(r"Hotspot\s*:\s*([\d\.]+)", page_text)
            coldspot_match = re.search(r"Coldspot\s*:\s*([\d\.]+)", page_text)

            if hotspot_match and coldspot_match:
                thermal_entries.append({
                    "page": i + 1,
                    "hotspot": float(hotspot_match.group(1)),
                    "coldspot": float(coldspot_match.group(1))
                })

    return thermal_entries


