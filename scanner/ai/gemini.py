import os
from google.genai import client

# Load Gemini API key from env
API_KEY = os.getenv("GEMINI_API_KEY")
client.configure(api_key=API_KEY)

def generate_fix(finding):
    prompt = f"""
You are a DevSecOps security expert.

Vulnerability details:
{finding}

Tasks:
1. Explain the vulnerability briefly
2. Provide secure fixed code (FULL FILE if code-based)
3. Provide best-practice advice

Return the response in JSON format:
{{
  "explanation": "...",
  "patched_code": "... or null"
}}
"""

    response = client.generate_text(
        model="gemini-1.5",
        prompt=prompt
    )

    return {
        "tool": finding["tool"],
        "file": finding.get("file"),
        "ai_response": response.text,
        "patched_code": response.text if finding["tool"] == "bandit" else None
    }
