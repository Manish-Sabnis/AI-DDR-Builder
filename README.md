# AI DDR Generator - Applied AI Workflow

## Overview

This project implements a reliability-focused AI workflow that converts raw inspection and thermal reports into a structured Detailed Diagnostic Report (DDR).

The system: 
- Extracts structured observations from inspection PDFs
- Uses OCR to process image-based thermal reports
- Combines both sources into structured evidence
- Generates a client-ready DDR using a constrained LLM
- Prevents hallucinated facts through strict prompt controls

## Architecture

The workflow is divided into four stages:

1)  Inspection Extraction Parses the summary table and extracts impacted-area observations.

2)  Thermal Extraction (OCR) Converts thermal PDF pages to images and extracts hotspot/coldspot values. Generates:
    - Average coldspot
    - Minimum coldspot
    - Total thermal images processed

3)  Correlation Layer Aggregates inspection findings and thermal summary into structured JSON. No assumptions or inferred mappings are added.

4)  Controlled AI Synthesis Uses a constrained LLM prompt to:
    - Avoid invented facts
    - Prevent unsupported severity escalation
    - Handle missing information explicitly
    - Produce structured Markdown DDR output

### Technologies
- Python
- pdfplumber
- pdf2image + pytesseract (OCR)
- Hugging Face Inference API (Mistral-7B)
- Markdown generation

### How to Run

1. Install dependencies: `pip install -r requirements.txt`

2. Install Tesseract OCR on your system.

3. Create `.env` file: `HF_TOKEN=your_huggingface_token_here`

4. Place inspection and thermal PDFs inside: data/

5. Run: `python src/main.py`

Output will be generated at: `outputs/DDR_Report.md`

## Limitations

-   Assumes similar summary table phrasing.
-   No automated conflict detection.
-   Thermal images are not spatially mapped to specific rooms.
-   OCR accuracy depends on image clarity.

## Design Focus

The system prioritizes: 
- Evidence-grounded reasoning
- Explicit handling of uncertainty
- Separation of extraction and synthesis
- Generalization to similar inspection reports

**The emphasis is on reliability and structured reasoning rather than UI complexity.**
