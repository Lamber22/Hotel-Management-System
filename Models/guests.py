"""from app import db
from billing import Billing

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=True)

def calculate_bill(self, nights):
        room_rates = {
            "Standard": 100,
            "Deluxe": 150,
            "Suite": 200
        }
        if self.room_type not in room_rates:
            return "Invalid room type"

        total_bill = room_rates[self.room_type] * nights
        billing = Billing(guest_id=self.id, amount=total_bill)
        db.session.add(billing)
        db.session.commit()
        return total_bill"""
        
from database import db
from Models.billing import Billing


class Guest(db.Model):
    __tablename__ = 'Guests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=True)

    def calculate_bill(self, nights):
        room_rates = {
            "Standard": 100,
            "Deluxe": 150,
            "Suite": 200
        }
        if self.room_type not in room_rates:
            return "Invalid room type"

        total_bill = room_rates[self.room_type] * nights
        billing = Billing(guest_id=self.id, amount=total_bill)
        db.session.add(billing)
        db.session.commit()
        return total_bill