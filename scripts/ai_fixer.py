import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key from .env or GitHub Secrets
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your environment.")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_remediation_from_ai(vuln_data):
    """Sends vulnerability details to Gemini and gets a code fix."""
    prompt = f"""
    You are a Senior DevSecOps Engineer. Fix the following security vulnerability:
    
    Vulnerability: {vuln_data.get('VulnerabilityID', 'Unknown')}
    Package: {vuln_data.get('PkgName', 'N/A')}
    Current Version: {vuln_data.get('InstalledVersion', 'N/A')}
    Fixed Version: {vuln_data.get('FixedVersion', 'N/A')}
    Description: {vuln_data.get('Description', 'No description provided')}
    
    Provide the fix in two parts:
    1. A brief explanation of the risk.
    2. The exact code or command to fix it.
    """
    
    response = model.generate_content(prompt)
    return response.text

def process_scan_results(input_json, output_md):
    with open(input_json, 'r') as f:
        scan_data = json.load(f)
    
    report_content = "# 🛡️ AI Security Remediation Report\n\n"
    
    # Iterate through scan results (Trivy format)
    for result in scan_data.get('Results', []):
        target = result.get('Target', 'Unknown File')
        report_content += f"## Target: `{target}`\n"
        
        for vuln in result.get('Vulnerabilities', []):
            ai_fix = get_remediation_from_ai(vuln)
            report_content += f"### 🔴 {vuln['VulnerabilityID']} in {vuln['PkgName']}\n"
            report_content += f"{ai_fix}\n\n"
            report_content += "---\n"

    with open(output_md, 'w') as f:
        f.write(report_content)
    print(f"Report generated: {output_md}")

if __name__ == "__main__":
    process_scan_results('scan_results.json', 'remediation_report.md')