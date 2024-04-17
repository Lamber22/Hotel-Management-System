from datetime import datetime
from flask import blueprints, request, jsonify, session, render_template
from sqlalchemy import false, true
from database import db
from datetime import datetime, timedelta


room_blueprint = blueprints.Blueprint('rooms', __name__, url_prefix='/api/v1/rooms')


class Room(db.Model):
    __tablename__ = 'Rooms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(20), nullable=False)
    room_price = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    available_date = db.Column(db.DateTime, nullable=False)


    @room_blueprint.route('/room_management', methods=['GET'])
    def room_management():
        return render_template('room.html')

def get_next_available_date(room_number):
    reservations = Reservation.query.filter_by(room_number=room_number).all()
    if not reservations:
        return datetime.utcnow()

    latest_checkout_date = max([reservation.check_out_date for reservation in reservations])
    return latest_checkout_date + timedelta(days=1)


def create_room(room_number, room_type, room_price):
    room = Room.query.filter_by(room_number=room_number).first()
    if room:
        #print(f"Room number {room_number} already exists, skipping.")
        return

    new_room = Room(
        room_number=room_number,
        room_type=room_type,
        room_price=room_price,
        is_available=True,
        available_date=get_next_available_date(room_number)
    )

    db.session.add(new_room)
    db.session.commit()


@room_blueprint.route('/count', methods=['GET'])
def room_count():
    is_available = request.args.get('is_available')
    if is_available == 'true':
        count = Room.query.filter_by(is_available=True).count()
    elif is_available == 'false':
        count = Room.query.filter_by(is_available=False).count()
    else:
        count = Room.query.count()
    return jsonify({'count': count})


@room_blueprint.route('/room-list', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_list = [{
        'id': room.id,
        'room_number': room.room_number,
        'room_type': room.room_type,
        'room_price': room.room_price,
        'is_available': room.is_available,
        'available_date': room.available_date,
        'reservations': [
            {
                'id': reservation.id,
                'guest_name': reservation.guest_name,
                'email': reservation.email,
                'phone': reservation.phone,
                'check_in_date': reservation.check_in_date.strftime('%Y-%m-%d'),
                'check_out_date': reservation.check_out_date.strftime('%Y-%m-%d'),
            }
            for reservation in room.reservations
        ],
    } for room in rooms]

    return jsonify(room_list)