# Installing packages
# to handle email sending via SMTP, the pip installations are included
# pip install smtplib
# pip install secure-smtplib

import smtplib  # Defines the SMTP protocol for email sending 
from email.mime.multipart import MIMEMultipart  # creates a multipart email message (header + body)
from email.mime.text import MIMEText  # Adds plain text content to the email body
import datetime  # Gets current date and time
import time  # Adds pauses between the email send attempts

# configuration constants for the email server
SMTP_SERVER = 'smtp.mail.com'  # The SMTP server to send emails
SMTP_PORT = 587  # Port number 587 for SMTP server
SENDER_EMAIL = 'hawialerts@hawibanks.com'  # Email address to send delayed alert
SENDER_PASSWORD = 'K6lly@0711'  # authenticates sender's email account
RECIPIENT_EMAIL = 'hawi@mail.com'  # Recipient email address for the alert

# Send emails with specified subject and body
def send_email(subject, body):
    try:
        # Connecting to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)  # Creating the SMTP object with server and port
        server.starttls()  # Starting TLS encryption for a secure connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Logging into sender's email account

        # Creating the email message with subject and body
        msg = MIMEMultipart()  # Creating the multipart message container
        msg['From'] = SENDER_EMAIL  # Setting the 'From' email address
        msg['To'] = RECIPIENT_EMAIL  # Setting the 'To' email address (recipient)
        msg['Subject'] = subject  # Setting subject of email
        msg.attach(MIMEText(body, 'plain'))  # Attaching body of email as plain text

        # Sending delayed alert email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())  # Sending the email
        print('Successfully sent!')  # Confirmation email sent

        # Closing connection to SMTP server
        server.quit()  # Closing SMTP connection to free up resources
    except Exception as err:
        # Handling errors that occur during email sending process
        print('Sending failed!', err)  # Printing the error message 

# monitor and send alerts based on realtime
def main():
    while True:  # loop to continuously check ideal time to send the email
        print("Alert when payment fails or is sent")  # Informing user of alert mechanism
        
        # Checking if current time is exactly 11:45 AM
        if datetime.datetime.now().hour == 11 and datetime.datetime.now().minute == 45:
            subject = 'Transaction Failed!'  # Setting subject of the email alert
            body = 'We are experiencing a systm challenge, Apologies. Try again later!'  # Setting mail body 
            send_email(subject, body)  # Calling send_email function 

        # Waiting for forty-five seconds, checks time again 
        time.sleep(45)  # Pauses loop execution for 45 seconds

# Execution of main function when sript runs 
if __name__ == '__main__':
    main()  # Starting loop, sending alerts based on schedule
