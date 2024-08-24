import os
from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
from Models.room import room_blueprint, create_room, Room
from Models.billing import bill_blueprint, Billing
import Blueprints
from datetime import datetime


app = Flask(__name__)
CORS(app)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)

app.register_blueprint(Blueprints.Reservations.reservation_blueprint)
app.register_blueprint(Blueprints.Admin.admin_blueprint)
app.register_blueprint(room_blueprint)
app.register_blueprint(bill_blueprint)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.home'))


if __name__ == '__main__':
    with app.app_context():
            db.create_all()

            create_room(101, 'Single', '50')
            create_room(102, 'Double', '70')
            create_room(103, 'Suite', '100')
            create_room(104, 'Deluxe', '120')
            create_room(105, 'Penthouse', '200')
            create_room(106, 'Penthouse', '200')
            create_room(107, 'Penthouse', '200')
            create_room(108, 'Penthouse', '200')
            create_room(109, 'Penthouse', '200')
            create_room(110, 'Penthouse', '200')

            app.run(debug=True)