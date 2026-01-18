import os
from google.genai import TextGenerationModel, TextGenerationRequest

# Option 1: Set environment variable directly
# Make sure GEMINI_API_KEY is set in env (CI or local)
API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GENAI_API_KEY"] = API_KEY

# Create model object
model = TextGenerationModel.from_pretrained("gemini-1.5")

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

    # Generate AI response
    response = model.predict(
        TextGenerationRequest(prompt=prompt)
    )

    return {
        "tool": finding["tool"],
        "file": finding.get("file"),
        "ai_response": response.candidates[0].content,
        "patched_code": response.candidates[0].content if finding["tool"] == "bandit" else None
    }
