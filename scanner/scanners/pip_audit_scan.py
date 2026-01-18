import json
import subprocess

def run_pip_audit():
    subprocess.run(
        ["pip-audit", "-f", "json", "-o", "pip-audit.json"],
        check=False
    )

    with open("pip-audit.json") as f:
        data = json.load(f)

    findings = []
    for dep in data.get("dependencies", []):
        for vuln in dep.get("vulns", []):
            findings.append({
                "tool": "pip-audit",
                "package": dep["name"],
                "installed_version": dep["version"],
                "issue": vuln["description"],
                "fix_versions": vuln.get("fix_versions")
            })

    return findings
