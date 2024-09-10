from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request, jsonify
from app.models import Transaction, Alert
from celery import Celery

#Database
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    error_message = Column(String)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    notification_channel = Column(String)
    notification_message = Column(String)

#APIs
app = Flask(__name__)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions])

@app.route('/alerts', methods=['POST'])
def send_alert():
    transaction_id = request.json['transaction_id']
    notification_channel = request.json['notification_channel']
    notification_message = request.json['notification_message']
    alert = Alert(transaction_id=transaction_id, notification_channel=notification_channel, notification_message=notification_message)
    db.session.add(alert)
    db.session.commit()
    return jsonify({'message': 'Alert sent successfully'})

#Send alerts

celery = Celery('tasks', broker='amqp://guest@localhost//')

@celery.task
def send_alert_async(transaction_id, notification_channel, notification_message):
    # Send alert using email, SMS, or other notification channels
    print(f'Sent alert for transaction {transaction_id} using {notification_channel}')
