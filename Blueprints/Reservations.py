from datetime import datetime
from flask import blueprints, request, redirect, jsonify, session, render_template
from database import db
from Models.room import Room
from Models.utils import calculate_bill
import json
import requests
import logging

reservation_blueprint = blueprints.Blueprint('reservations', __name__, url_prefix='/api/v1/reservations')


class Reservation(db.Model):
    __tablename__ = 'Reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('reservations', lazy=True))
    billing = db.relationship('Billing', uselist=False, back_populates='guest')

    @staticmethod
    def is_room_available(room_number, check_in_date, check_out_date):
        reservations = Reservation.query.filter(
            Reservation.room_number == room_number,
            Reservation.check_out_date >= check_in_date
        ).all()

        for reservation in reservations:
            if reservation.check_in_date <= check_in_date <= reservation.check_out_date:
                return False

        return True


@reservation_blueprint.route('/', methods=['POST'])
def make_reservation():
    from Models.billing import Billing  # Import here to avoid circular import
    try:
        data = request.form
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'check_in_date', 'check_out_date', 'room_number']
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Incomplete form data"}), 400

        guest_name = f"{data['first_name']} {data['last_name']}"
        email = data['email']
        phone = data['phone']

        try:
            check_in_date = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format"}), 400

        try:
            room_number = int(data['room_number'])
            room = Room.query.filter_by(room_number=room_number).first()
            if not room:
                return jsonify({"message": "Room not found"}), 404

        except ValueError:
            return jsonify({"message": "Room number must be an integer"}), 400

        if not Reservation.is_room_available(room_number, check_in_date, check_out_date):
            return jsonify({"message": "Room not available for the specified dates"}), 400

        headers = {'Content-Type': 'application/json'}
        url = 'http://localhost:5000/api/v1/billing/calculate_bill'
        bill_data = {
            'room_type': room.room_type,
            'check_in_date': check_in_date.strftime('%Y-%m-%d'),
            'check_out_date': check_out_date.strftime('%Y-%m-%d')
        }
        response = requests.post(url, data=json.dumps(bill_data), headers=headers)

        print(response.json())
        bill_amount = response.json().get('amount')  # Get amount from response
        new_billing = Billing(
            id=None,
            amount=bill_amount
        )

        reservation = Reservation(
            guest_name=guest_name,
            email=email,
            phone=phone,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            room_number=room_number,
            room_id=room.id,
            billing=new_billing.id
        )

        new_billing.guest_id = reservation.id
        db.session.add(reservation)
        db.session.add(new_billing)
        db.session.commit()

        room = Reservation.query.filter_by(room_number=room_number).first().room
        room.is_available = False
        room.available_date = check_out_date
        db.session.commit()

        return render_template('admin_dashboard.html',
                            guest_name=guest_name,
                            email=email,
                            phone=phone,
                            check_in_date=check_in_date.strftime('%Y-%m-%d'),
                            check_out_date=check_out_date.strftime('%Y-%m-%d'),
                            room_number=room_number)

    except Exception as e:
        logging.error(f"Error occurred during reservation creation: {str(e)}")
        return jsonify({"message": str(e)}), 500


@reservation_blueprint.route('/api/reservations', methods=['GET'])
def get_reservations_api():
    try:
        reservations = Reservation.query.all()
        reservations_data = []
        for reservation in reservations:
            reservations_data.append({
                "guest_name": reservation.guest_name,
                "email": reservation.email,
                "phone": reservation.phone,
                "checkin_date": reservation.check_in_date.strftime('%Y-%m-%d'),
                "checkout_date": reservation.check_out_date.strftime('%Y-%m-%d'),
                "room_number": reservation.room_number,
            })
        return jsonify(reservations_data)

    except Exception as e:
        print(e)
        logging.error(f"Error occurred while fetching reservations: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request"}), 500

@reservation_blueprint.route('/<int:id>', methods=['DELETE'])
def cancel_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404

    room = reservation.room
    room.is_available = False
    room.available_date = datetime.utcnow()

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation cancelled successfully"}), 204

@reservation_blueprint.route('/check_in')
def reservation_checkin():
    try:
        reservations = Reservation.query.all()
        return render_template('check_in.html', reservations=reservations)

    except Exception as e:
        print(e)
        logging.error(f"Error occurred while fetching reservations: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request"}), 500

@reservation_blueprint.route('/check_out')
def reservation_checkout():
    return render_template('check_out.html')

@reservation_blueprint.route('view_reservation')
def view_reservation():
    return render_template('view_reservation.html')


