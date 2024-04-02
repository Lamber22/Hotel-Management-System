from datetime import datetime
from flask import blueprints, request, jsonify
from sqlalchemy import false, true

from Models.room import Room
from database import db

room_blueprint = blueprints.Blueprint('rooms', __name__, url_prefix='/api/v1/rooms')

@room_blueprint.route('/', methods=['POST'])
def create_room():
    data = request.json
    room_number = data['room_number']
    room_type = data['room_type']
    room_price = data['room_price']

    room = Room(room_number=room_number, room_type=room_type, room_price=room_price,
                is_available=true, available_date=datetime.now())
    db.session.add(room)
    db.session.commit()

    return jsonify({"message": "Room created successfully"}), 201

@room_blueprint.route('/', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_list = [{
        'room_number': room.room_number,
        'room_type': room.room_type,
        'room_price': room.room_price
    } for room in rooms]

    return jsonify(room_list), 200


@room_blueprint.route('/<int:id>', methods=['GET'])
def get_room(number):
    room = Room.query.filter_by(room_number=number).first()
    if not room:
        return jsonify({"message": "Room not found"}), 404

    return jsonify({
        'room_number': room.room_number,
        'room_type': room.room_type,
        'room_price': room.room_price
    }), 200


@room_blueprint.route('/', methods=['PUT'])
def update_room():
    data = request.json
    room_number = data['room_number']
    room_price = data['room_price']
    is_available = data['is_available']
    available_date = datetime.strptime(data['available_date'], '%Y-%m-%d').date()

    room = Room.query.filter_by(room_number=room_number).first()
    if not room:
        return jsonify({"message": "Room not found"}), 404

    room.room_price = room_price
    room.is_available = true if is_available == 'Yes' else false
    room.available_date = available_date
    db.session.commit()

    return jsonify({"message": "Room updated successfully"}), 200