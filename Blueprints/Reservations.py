import logging
from datetime import datetime

from flask import blueprints, request, jsonify, render_template

from Models.room import Room
from database import db

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


def is_room_available(room_number, check_in_date, check_out_date):
    reservations = Reservation.query.filter(
        Reservation.room_number == room_number,
        Reservation.check_in_date <= check_out_date,
        Reservation.check_out_date >= check_in_date
    ).all()

    if reservations:
        return False
    else:
        return True


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
    room.is_available = True
    room.available_date = None

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
def reservation_checkout(self):
    return render_template('check_out.html')


@reservation_blueprint.route('/', methods=['POST'])
def make_reservation():
    try:
        data = request.form
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'check_in_date', 'check_out_date',
                           'room_number']
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
            return jsonify({"message": "Room number Must be a integer"}), 400

        if not Reservation.is_room_available(room_number, check_in_date, check_out_date):
            return jsonify({"message": "Room not available for the specified dates"}), 400

        reservation = Reservation(
            guest_name=guest_name,
            email=email,
            phone=phone,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            room_number=room_number,
            room_id=room.id
        )

        db.session.add(reservation)
        db.session.commit()

        room = Reservation.query.filter_by(room_number=room_number).first().room
        room.is_available = False
        db.session.commit()

        return render_template('admin_dashboard.html',
                               guest_name=guest_name,
                               email=email,
                               phone=phone,
                               check_in_date=check_in_date.strftime('%Y-%m-%d'),
                               check_out_date=check_out_date.strftime('%Y-%m-%d'),
                               room_number=room_number)

    except Exception as e:
        print(e)
        logging.error(f"Error occurred during reservation creation: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request"}), 500
