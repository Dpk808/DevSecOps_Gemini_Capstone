import os
import json
from datetime import datetime

def write_report(findings, fixes):
    os.makedirs("reports", exist_ok=True)

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "findings": findings,
        "ai_fixes": fixes
    }

    with open("reports/security_report.json", "w") as f:
        json.dump(report, f, indent=2)
