import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_otp_email(email: str, otp: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = "SkipTheLine - Your OTP Code"

    body = f"""
    Hi there,

    Your SkipTheLine OTP is: {otp}

    Valid for 10 minutes.
    Do not share this code.

    Thanks,
    SkipTheLine Team 🍽️
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False
