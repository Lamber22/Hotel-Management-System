from database import db


class Billing(db.Model):
    __tablename__ = 'Billing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('Guests.id'))
    amount = db.Column(db.Integer, nullable=False)
    guest = db.relationship("Guest", back_populates="billing")
"""from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from guests import Guest

billing_bp = Blueprint('billing', __name__)

class Billing(db.Model):
    __tablename__ = 'billing'
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    data = request.json
    guest_name = data.get('guest_name')
    room_type = data.get('room_type')
    nights = data.get('nights')

    if not all([guest_name, room_type, nights]):
        return "Missing required data", 400

    guest = Guest.query.filter_by(name=guest_name).first()
    if not guest:
        return "Guest not found", 404

    guest.room_type = room_type
    total_bill = guest.calculate_bill(nights)

    return {
        "Guest Name": guest_name,
        "Room Type": room_type,
        "Nights": nights,
        "Total Bill": total_bill
    }

"""
