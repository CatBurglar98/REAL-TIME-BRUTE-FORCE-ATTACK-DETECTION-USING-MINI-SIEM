from flask import Flask, render_template, request, redirect, session
import pyotp
import json
import os
from datetime import datetime
from siem_engine import analyze_log

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

AUTH_LOG = "logs/auth.log"
ALERT_LOG = "logs/alerts.log"

# FIXED SECRET (so it doesn’t change every restart)
USER_DB = {
    "admin": {
        "password": "password123",
        "mfa_secret": "JBSWY3DPEHPK3PXP"
    }
}

# Function to write logs
def write_log(event_type, username, status, ip):
    log_entry = {
        "timestamp": str(datetime.now()),
        "event_type": event_type,
        "username": username,
        "status": status,
        "ip": ip
    }

    with open(AUTH_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    analyze_log(log_entry)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr

        if username in USER_DB and USER_DB[username]["password"] == password:
            session["username"] = username
            write_log("LOGIN", username, "SUCCESS", ip)
            return redirect("/mfa")
        else:
            write_log("LOGIN", username, "FAILED", ip)
            return "Login Failed"

    return render_template("login.html")


@app.route("/mfa", methods=["GET", "POST"])
def mfa():
    if "username" not in session:
        return redirect("/")

    username = session["username"]
    totp = pyotp.TOTP(USER_DB[username]["mfa_secret"])

    if request.method == "POST":
        token = request.form["token"]
        ip = request.remote_addr

        if totp.verify(token):
            write_log("MFA", username, "SUCCESS", ip)
            return redirect("/dashboard")
        else:
            write_log("MFA", username, "FAILED", ip)
            return "MFA Failed"

    return render_template("mfa.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    success = 0
    failed = 0

    if os.path.exists(AUTH_LOG):
        with open(AUTH_LOG) as f:
            for line in f:
                data = json.loads(line)
                if data["status"] == "SUCCESS":
                    success += 1
                else:
                    failed += 1

    logs = []
    if os.path.exists(AUTH_LOG):
        with open(AUTH_LOG) as f:
            logs = f.readlines()

    return render_template(
        "dashboard.html",
        success=success,
        failed=failed,
        logs=logs
    )


if __name__ == "__main__":
    app.run(debug=True)
