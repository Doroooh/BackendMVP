# Installing packages
# the pip installations will  handle email sending via SMTP
# pip install smtplib
# pip install secure-smtplib

pip install smtplib the Module to define SMTP protocol to send emails
pip install secure-smtplib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time

# the email configuration
SMTP_SERVER = 'smtp.mail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'hawialerts@hawibanks.com'
SENDER_PASSWORD = 'K6lly@0711'
RECIPIENT_EMAIL = 'hawi@mail.com'


def send_email(subject, body):
    try:
        # Connecting to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Composing the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Sending the email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print('Successfully sent!')

        # Closing the connection
        server.quit()
    except Exception as err:
        print('Sending failed:', err)

def main():
    while True:
        print("Alerts when a payment fails or is sent")
        # Checking if the current time is 9:00 AM
        if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 0:
            subject = 'Failed Transaction Alerts'
            body = 'Apologies for the system error, Try again later!'
            send_email(subject, body)

        # If sending failed, resend later after thirty seconds 
        time.sleep(30)

if __name__ == '__main__':
    main()
