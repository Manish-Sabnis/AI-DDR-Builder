import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables.")

client = InferenceClient(api_key=HF_TOKEN)

MODEL = "mistralai/Mistral-7B-Instruct-v0.2:cheapest"


def generate_ddr(correlated_data):
    """
    Generates a Detailed Diagnostic Report (DDR)
    using structured inspection + thermal data.
    """

    structured_json = json.dumps(correlated_data, indent=2)

    prompt = f"""
You are a structured building diagnostics report generator.

Use ONLY the information provided in the JSON below.
Do NOT use external knowledge.
Do NOT assume additional damage.
Do NOT increase severity unless explicitly supported by the data.

Structured Data (JSON):
{structured_json}

Instructions:

- Only describe issues explicitly listed in inspection_findings.
- Use thermal_summary strictly as supporting evidence.
- If thermal_summary contains temperature values, you may mention that lower coldspot readings suggest moisture presence.
- Do NOT classify severity as High unless the structured data explicitly indicates severe damage.
- If severity cannot be determined from the data, classify as "Moderate" and state that limited evidence is available.
- If information is missing, write "Not Available".

Generate the report in clean Markdown format with the following sections:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (based strictly on given data)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information
"""


    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You generate structured building diagnostic reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200,
    )

    return completion.choices[0].message.content
