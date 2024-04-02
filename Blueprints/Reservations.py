from datetime import datetime
from flask import blueprints, request, jsonify
from Models.reservation import Reservation
from database import db
from Models.room import Room

reservation_blueprint = blueprints.Blueprint('reservations', __name__, url_prefix='/api/v1/reservations')


@reservation_blueprint.route('/', methods=['POST'])
def make_reservation():
    data = request.json
    guest_name = f"{data['first_name']} {data['last_name']}"
    email = data['email']
    phone = data['phone']
    check_in_date = datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
    check_out_date = datetime.strptime(data['check_out_date'], '%Y-%m-%d').date()
    room_number = data['room_number']

    room = Room.query.filter_by(room_number=room_number).first()
    if not room:
        return jsonify({"message": "Room not found"}), 404

    # check room availability
    if not room.is_available:
        return jsonify({"message": "Room not available"}), 400

    room.is_available = False
    room.available_date = check_out_date

    reservation = Reservation(guest_name=guest_name, email=email, phone=phone,
                              check_in_date=check_in_date, check_out_date=check_out_date,
                              room_number=room_number)

    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation made successfully"}), 200


@reservation_blueprint.route('/', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    reservation_list = [{
        'guest_name': reservation.guest_name,
        'email': reservation.email,
        'phone': reservation.phone,
        'check_in_date': reservation.check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': reservation.check_out_date.strftime("%Y-%m-%d"),
        'room_number': reservation.room_number
    } for reservation in reservations]

    return jsonify(reservation_list), 200


@reservation_blueprint.route('/<int:id>', methods=['GET'])
def get_reservation(guest_name):
    reservation = Reservation.query.filter_by(guest_name=guest_name)
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404

    return jsonify({
        'id': reservation.id,
        'guest_name': reservation.guest_name,
        'email': reservation.email,
        'phone': reservation.phone,
        'check_in_date': reservation.check_in_date.strftime("%Y-%m-%d"),
        'check_out_date': reservation.check_out_date.strftime("%Y-%m-%d"),
        'room_number': reservation.room_number
    }), 200


@reservation_blueprint.route('/<int:id>', methods=['DELETE'])
def cancel_reservation(id):
    reservation = Reservation.query.get(id).join(Room).filter(Room.room_number == Reservation.room_number).first()
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404

    reservation.room.is_available = True
    reservation.room.available_date = None

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation cancelled successfully"}), 204