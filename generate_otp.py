import smtplib
import math, random


def generate_opt(email):
  digits = "0123456789"
  OTP = ""
  for i in range(4):
    OTP += digits[math.floor(random.random() * 10)]
  print("OTP Generated is:", OTP)
  smtp_server = 'smtp.gmail.com'
  smtp_port = 587
  smtp_username = 'awstestuser1998@gmail.com'
  smtp_password = 'vynz sffl mhsj zydv'

  to_email = email
  subject = 'OTP Verification'
  from_email = 'awstestuser1998@gmail.com'
  subject = 'Hello, world!'
  body = f'This is a test email.{OTP}'

  message = f'Subject: {subject}\n\n{body}'

  with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(from_email, to_email, message)
  return OTP
