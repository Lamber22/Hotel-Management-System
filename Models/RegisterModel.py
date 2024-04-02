from flask import Flask, request, jsonify, Blueprint, render_template, redirect
from app import db
from models import Staff

registration_bp = Blueprint('registration', __name__)


@app.route('/register', methods=['POST'])
def register():
    if 'name' in request.form:
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        salary = float(request.form['salary'])
        date_of_birth = request.form['date_of_birth']
        tel = request.form['tel']
        address = request.form['address']
        date_of_employment = request.form['date_of_employment']

        new_staff = Staff(name=name, position=position, email=email, salary=salary, 
                          date_of_birth=date_of_birth, tel=tel, address=address,
                          date_of_employment=date_of_employment)
        db.session.add(new_staff)
        db.session.commit()

        return redirect('/staff_list')
    

    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone_number = request.form['phone_number']
        
        new_staff = Staff(username=username, email=email, password=password, 
                          confirm_password=confirm_password, phone_number=phone_number)
        db.session.add(new_staff)
        db.session.commit()
        
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
