# REAL-TIME-BRUTE-FORCE-ATTACK-DETECTION-USING-MINI-SIEM
A Mini SIEM system to detect brute-force login attacks in real time. A Flask-based app logs authentication events, while a Python attack script simulates repeated failures. The SIEM analyzes logs, detects suspicious activity, and generates dashboard alerts with visual metrics for SOC-style monitoring.

# Install Dependencies
pip install flask pyotp requests


If using Linux/Kali:

pip3 install flask pyotp requests

# Run the Application
python app.py


You should see:

Running on http://127.0.0.1:5000


Open browser and go to:

http://127.0.0.1:5000

# Login Credentials
Username: admin
Password: password123

 Generate OTP for MFA

# Open a new terminal:

python


Then run:

import pyotp
totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
print(totp.now())


Enter the generated 6-digit OTP on the MFA page.

Testing Brute Force Detection
Manual Method

Login with correct username/password

On MFA page enter wrong OTP (e.g., 000000)

Repeat 3+ times

After threshold is reached, terminal will show:

[ALERT] MFA Abuse detected from IP: 127.0.0.1

# Automatic Attack Simulation

Run:

python attack_simulator.py


This script simulates repeated failed MFA attempts.

# View Dashboard

Go to:

http://127.0.0.1:5000/dashboard


# Dashboard displays:

Authentication success/failure metrics

Pie chart visualization

Raw authentication logs

# Log Files
Authentication Logs
logs/auth.log


Contains:

LOGIN events

MFA events

SUCCESS / FAILED status

IP address

Timestamp

# Alert Logs
logs/alerts.log


Contains:

Alert type

Trigger reason

IP address

Timestamp
