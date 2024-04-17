from flask import jsonify, request, redirect, session
from datetime import datetime
import json
import requests
from Models import billing


def calculate_bill(bill_data):
    room_type = bill_data['room_type']
    check_in_date = bill_data['check_in_date']
    check_out_date = bill_data['check_out_date']

    room_rates = {
        'Single': 50,
        "Double": 70,
        "Deluxe": 120,
        "Penthouse": 200,
        "Suite": 100
    }

    room_rate = room_rates[room_type]
    length_of_stay = (datetime.strptime(check_out_date, '%Y-%m-%d') - datetime.strptime(check_in_date, '%Y-%m-%d')).days
    amount = room_rate * length_of_stay

    return jsonify({'amount': amount})
