import os
from scanners.bandit_scan import run_bandit
from scanners.pip_audit_scan import run_pip_audit
from ai.gemini import generate_fix
from dotenv import load_dotenv
load_dotenv()
from utils.report import write_report

APPLY_FIXES = os.getenv("APPLY_FIXES", "false").lower() == "true"

findings = []
fixes = []

print("[+] Running Bandit scan...")
findings.extend(run_bandit())

print("[+] Running pip-audit scan...")
findings.extend(run_pip_audit())

for finding in findings:
    ai_fix = generate_fix(finding)
    fixes.append(ai_fix)

    if APPLY_FIXES and ai_fix.get("patched_code"):
        print(f"[!] Applying fix to {ai_fix['file']}")
        with open(ai_fix["file"], "w") as f:
            f.write(ai_fix["patched_code"])

write_report(findings, fixes)
print("[+] Security scan completed.")
