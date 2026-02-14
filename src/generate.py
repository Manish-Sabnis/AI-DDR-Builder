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
Do NOT use external domain knowledge.
Do NOT assume construction defects, settlement, installation errors, or hidden structural causes unless explicitly stated in the data.

Structured Data (JSON):
{structured_json}

Inference Rules:
- If tile joint gaps are observed, you may state that they allow potential moisture ingress.
- If cracks on external walls are observed, you may state that they may allow water penetration.
- Do NOT speculate about settlement, structural movement, or installation quality.
- Do NOT escalate severity beyond what is supported by the data.
- Default severity to "Moderate" unless explicitly described as mild or severe.
- Thermal coldspot values may indicate possible moisture presence.
- If thermal location mapping is not available, explicitly state that correlation to specific areas is not available.
- If any required information is missing, write "Not Available".

Generate the report in clean Markdown format with these exact sections:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause (strictly mechanism-based, no speculation)
4. Severity Assessment (based only on provided evidence)
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
