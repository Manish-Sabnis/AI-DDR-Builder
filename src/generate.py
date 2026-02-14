import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"


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

    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 900,
            "temperature": 0.2
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()
    return result[0]["generated_text"]
