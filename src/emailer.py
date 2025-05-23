import smtplib
from email.mime.text import MIMEText
import yaml
import os

def load_email_config(path="config/email_config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def send_email(subject, body, config_path="config/email_config.yaml"):
    config = load_email_config(config_path)
    
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = config["sender_email"]
    msg["To"] = config["receiver_email"]

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(config["sender_email"], config["sender_pass"])
            server.sendmail(config["sender_email"], config["receiver_email"], msg.as_string())
        print("[✔] Email sent.")
    except Exception as e:
        print(f"[✘] Failed to send email: {e}")
