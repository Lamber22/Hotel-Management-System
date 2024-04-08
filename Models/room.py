"""from database import db


class Room(db.Model):
    __tablename__ = 'Rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    available_date = db.Column(db.Date)
    reservations = db.relationship("Reservation", back_populates="room")

    @classmethod
    def insert_rooms(cls):
        rooms_data = [
            {'room_number': '101', 'room_type': 'Single', 'price_per_night': 50.0},
            {'room_number': '102', 'room_type': 'Double', 'price_per_night': 80.0},
            {'room_number': '103', 'room_type': 'Suite', 'price_per_night': 120.0}
        ]

        for room_info in rooms_data:
            room = cls(**room_info)
            db.session.add(room)

        db.session.commit()"""