from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

class Booking(db.Model):
    __tablename__ = 'Booking'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    check_in_date = db.Column(db.DateTime, nullable=False)
    check_out_date = db.Column(db.DateTime, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

@app.route('/booking', methods=['POST'])
def make_booking():
    data = request.json
    customer_name = data['customer_name']
    check_in_date = datetime.strptime(data['check_in_date'], '%Y-%m-%d')
    check_out_date = datetime.strptime(data['check_out_date'], '%Y-%m-%d')
    room_id = data['room_id']

    booking = Booking(customer_name=customer_name, check_in_date=check_in_date,
                      check_out_date=check_out_date, room_id=room_id)
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking made successfully"}), 200

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = [{
        'id': booking.id,
        'customer_name': booking.customer_name,
        'check_in_date': booking.check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': booking.check_out_date.strftime("%Y-%m-%d"),
        'room_id': booking.room_id
    } for booking in bookings]

    return jsonify(booking_list), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
