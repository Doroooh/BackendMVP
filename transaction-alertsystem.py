# Importing libraries for the project
from flask import Flask, jsonify  # Flask for creating the web app, jsonify to return JSON responses
import smtplib  # SMTP protocol for email sending
from email.mime.multipart import MIMEMultipart  # Creates a multipart email (header + body)
from email.mime.text import MIMEText  # Adds plain text content to the email body
import datetime  # Handling date and time operations
import time  # Adding pauses and execution delays
import MySQLdb  # MySQLdb package to connect Flask with MySQL database

# Initializing Flask application
app = Flask(__name__)

# MySQL database configuration 
app.config['MYSQL_HOST'] = 'localhost'  # Host where MySQL is running
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # MySQL password
app.config['MYSQL_DB'] = 'transactions_db'  # Name of the database

# Establishing connection to MySQL database using MySQLdb
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="password",
    db="transactions_db"
)

# Configuring email sending features
SMTP_SERVER = 'smtp.mail.com'  # SMTP server that sends emails
SMTP_PORT = 587  # Port for SMTP server
SENDER_EMAIL = 'hawialerts@hawibanks.com'  # Sender email address
SENDER_PASSWORD = 'K6lly@0711'  # Password for sender's email account
RECIPIENT_EMAIL = 'hawi@mail.com'  # Email address of user receiving alerts

# Function that sends email with subject and body using SMTP server
def send_email(subject, body):
    try:
        # Creating an SMTP session to send emails
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.startssl()  # Enabling security by starting TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the SMTP server with sender's credentials

        # Creating a MIMEMultipart message to structure the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL  # Setting sender's email
        msg['To'] = RECIPIENT_EMAIL  # Setting the recipient's email
        msg['Subject'] = subject  # Setting email subject
        msg.attach(MIMEText(body, 'plain'))  # Attaching email body as plain text

        # Sending email using the SMTP server
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print('Email successfully sent!')  # Confirm email sent successfully

        # Closing connection to SMTP server
        server.quit()
    except Exception as err:
        # If fails, print the error message
        print('Failed to send email!', err)

# Flask route to check failed transactions in database
@app.route('/check_transactions', methods=['GET'])
def check_transactions():
    cursor = db.cursor()  # Creating cursor object for executing MySQL queries

    # SQL query that retrieves transactions where transaction status is 'failed'
    query = "SELECT id, amount, status FROM transactions WHERE status='failed'"
    cursor.execute(query)  # Executing SQL query
    failed_transactions = cursor.fetchall()  # Fetching all results of the query

    # If transaction failed, send email alert
    if failed_transactions:
        subject = 'Transaction Failed!'  # Setting email subject
        body = 'We are experiencing a system challenge. Apologies. Try again later!'  # Setting email body content
        send_email(subject, body)  # Sending the email notification

        # Returning a JSON response with list of failed transactions and confirmation
        return jsonify({
            'message': 'Email sent to notify failed transactions!',
            'transactions': failed_transactions
        }), 200
    else:
        # If all transactions successful, return the JSON response indicating all successful
        return jsonify({
            'message': 'Transactions successful!'
        }), 200

# Creates necessary database and tables if not existing
@app.before_first_request
def setup_db():
    cursor = db.cursor()  # Creating cursor object to execute MySQL queries

    # SQL query to create the 'transactions_db' database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS transactions_db")
    
    # SQL query to create the 'transactions' table for storing transaction records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2),  # Stores the transaction amount
            status VARCHAR(255)  # Stores the transaction status ('success', 'failed', etc.)
        )
    """)
    db.commit()  # Commit the changes to the database

# function to periodically check time and trigger alerts for failed transactions
def monitor_transactions():
    while True:
        print("Checking for failed transactions...")  # the log to indicate system is monitoring transactions
        current_time = datetime.datetime.now()  # Get current date and time

        # If the current time is 11:45 AM, trigger the check for failed transactions
        if current_time.hour == 11 and current_time.minute == 45:
            check_transactions()  # Calling the check_transactions function to monitor the database

        # Pausing loop for 45 seconds before checking again
        time.sleep(45)

# The main entry point of the script - Flask app starts running and the monitoring loop begins
if __name__ == '__main__':
    monitor_transactions()  # Starting transaction monitoring loop
    app.run(debug=True)  # Starting Flask application in debug mode
