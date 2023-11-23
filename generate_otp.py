import smtplib
import math, random
import os


def generate_opt(email, user):
  digits = "0123456789"
  OTP = ""
  for i in range(4):
    OTP += digits[math.floor(random.random() * 10)]
  print("OTP Generated is:", OTP)
  smtp_server = 'smtp.gmail.com'
  smtp_port = 587
  smtp_username = os.getenv("gmail")
  smtp_password = os.getenv("gmail_pass")
  print(smtp_username)
  print(smtp_password)

  to_email = email
  subject = 'OTP Verification'
  from_email = smtp_username
  subject = 'Hello, world!'
  body = f"""
Dear {user},

As per your password reset request below is the OTP for verification.  
OTP: {OTP}

Please do not share the OTP with anyone!
  
Thanks,
PyVaultcorp.
  
  Please do not reply!  This is a system generated mail"""

  message = f'Subject: {subject}\n\n{body}'

  with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(from_email, to_email, message)
  return OTP
