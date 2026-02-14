# Data Folder

This folder is intended for input inspection and thermal reports.

Expected files:
- Inspection Report (structured PDF)
- Thermal Report (image-based PDF with hotspot and coldspot readings)

Example:
- `data/Sample_Report.pdf`
- `data/Thermal_Images.pdf`

Note:
Input PDFs are not included in this repository due to confidentiality.

The system expects:
- Inspection reports containing a summary table with "`Observed ... of Flat No. XXX`" format.
- Thermal reports containing hotspot and coldspot temperature readings per image.

Place the required PDF files in this folder before running: `python src/main.py`
