import json
from collections import defaultdict
from datetime import datetime

ALERT_LOG = "logs/alerts.log"

failed_mfa_counter = defaultdict(int)

def analyze_log(log_entry):
    if log_entry["event_type"] == "MFA" and log_entry["status"] == "FAILED":
        ip = log_entry["ip"]
        failed_mfa_counter[ip] += 1

        if failed_mfa_counter[ip] >= 3:
            alert = {
                "timestamp": str(datetime.now()),
                "alert_type": "MFA_ABUSE",
                "ip": ip,
                "message": "Multiple failed MFA attempts detected"
            }

            with open(ALERT_LOG, "a") as f:
                f.write(json.dumps(alert) + "\n")

            print("[ALERT] MFA Abuse detected from IP:", ip)
