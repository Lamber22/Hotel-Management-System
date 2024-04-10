from datetime import datetime
from flask import blueprints, request, redirect, jsonify, session, render_template
from database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import logging
#from Models.room import Room

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




    @reservation_blueprint.route('/', methods=['POST'])
    def make_reservation():
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
            except ValueError:
                return jsonify({"message": "Invalid room number"}), 400

            reservation = Reservation(
                guest_name=guest_name,
                email=email,
                phone=phone,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                room_number=room_number
            )

            db.session.add(reservation)
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
    def reservation_checkout():
        return render_template('check_out.html')