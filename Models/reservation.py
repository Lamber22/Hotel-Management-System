from database import db


class Reservation(db.Model):
    __tablename__ = 'Reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_number = db.Column(db.String(50), nullable=False)

    room = db.relationship("Room", back_populates="reservation")