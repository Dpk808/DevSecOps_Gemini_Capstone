import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_fix(finding):
    prompt = f"""
You are a DevSecOps security expert.

Vulnerability details:
{finding}

Tasks:
1. Explain the vulnerability briefly
2. Provide secure fixed code (FULL FILE if code-based)
3. Provide best-practice advice

Return the response in this JSON format:
{{
  "explanation": "...",
  "patched_code": "... or null"
}}
"""

    response = model.generate_content(prompt)

    return {
        "tool": finding["tool"],
        "file": finding.get("file"),
        "ai_response": response.text,
        "patched_code": response.text if finding["tool"] == "bandit" else None
    }
