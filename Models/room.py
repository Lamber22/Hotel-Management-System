from database import db


class Room(db.Model):
    __tablename__ = 'Rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    available_date = db.Column(db.Date, nullable=False)

    reservation = db.relationship("Reservation", back_populates="room", uselist=False)