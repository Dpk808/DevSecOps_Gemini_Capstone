import json
import subprocess

def run_bandit():
    subprocess.run(
        ["bandit", "-r", ".", "-f", "json", "-o", "bandit.json"],
        check=False
    )

    with open("bandit.json") as f:
        data = json.load(f)

    findings = []
    for issue in data.get("results", []):
        findings.append({
            "tool": "bandit",
            "file": issue["filename"],
            "line": issue["line_number"],
            "issue": issue["issue_text"],
            "severity": issue["issue_severity"],
            "code": issue["code"]
        })

    return findings
