from datetime import datetime, timedelta
from flask import blueprints, request, redirect, jsonify, session, render_template
from Blueprints.Reservations import Reservation
from database import db
from Models import billing
from Models.utils import calculate_bill
import json
import requests


bill_blueprint = blueprints.Blueprint('billing', __name__, url_prefix='/api/v1/billing')

class Billing(db.Model):
    __tablename__ = 'Billing'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_name = db.Column(db.Integer, db.ForeignKey('Reservations.id'))
    amount = db.Column(db.Integer, nullable=False)
    guest = db.relationship(Reservation, back_populates="billing")



@bill_blueprint.route('/calculate_bill', methods=['POST'])
def calculate_bill_route():
    bill_data = request.get_json()
    return calculate_bill(bill_data)


@bill_blueprint.route('/get_bills')
def get_bills():
    bills = Billing.query.all()
    bill_list = []
    for bill in bills:
        reservation = Reservation.query.get(bill.id)
        if reservation is not None:
            check_out_date = reservation.check_out_date
            check_in_date = reservation.check_in_date
            number_of_nights = (check_out_date - check_in_date).days
            bill_list.append({
                'guestName': reservation.guest_name,
                'numberOfNights': number_of_nights,
                'bill': bill.amount,
                'roomNo': reservation.room_number,
                'status': 'Active' if check_out_date > datetime.datetime.now() else 'Checked Out'
            })
    return jsonify(bill_list)

@bill_blueprint.route('/view_bills')
def view_bills():
    bills = Billing.query.all()
    bill_list = []
    for bill in bills:
        reservation = Reservation.query.get(bill.guest_name)
        if reservation is not None:
            check_out_date = reservation.check_out_date
            check_in_date = reservation.check_in_date
            number_of_nights = (check_out_date - check_in_date).days
            bill_list.append({
                'guestName': reservation.guest_name,
                'numberOfNights': number_of_nights,
                'bill': bill.amount,
                'roomNo': reservation.room_number,
                'status': 'Active' if check_out_date > datetime.now() else 'Checked Out'
            })
    return render_template('billing.html', billings=bill_list)



Reservation.calculate_bill = calculate_bill