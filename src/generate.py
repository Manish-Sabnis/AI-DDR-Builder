import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"]
)

MODEL = "mistralai/Mistral-7B-Instruct-v0.2:cheapest"


def generate_ddr(correlated_data):
    prompt = f"""
You are a building diagnostic assistant.

Using ONLY the structured data below, generate a Detailed Diagnostic Report.

Structured Data:
{correlated_data}

Rules:
- Do NOT invent facts.
- If information is missing, write "Not Available".
- Use simple client-friendly language.
- Include:
  1. Property Issue Summary
  2. Area-wise Observations
  3. Probable Root Cause
  4. Severity Assessment (with reasoning)
  5. Recommended Actions
  6. Additional Notes
  7. Missing or Unclear Information
"""

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=900,
    )

    return completion.choices[0].message.content
