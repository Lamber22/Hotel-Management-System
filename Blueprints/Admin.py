from functools import wraps
from os import getenv
from flask import blueprints, request, redirect, session, render_template

admin_blueprint = blueprints.Blueprint('login', __name__, url_prefix='/api')


def admin_login_required(f):
    @wraps(f)
    def admin_login_check(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect('/admin_login')
        return f(*args, **kwargs)

    return admin_login_check


@admin_blueprint.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = getenv('ADMIN_NAME')
        password = getenv('ADMIN_PASSWD')
        if request.form['username'] == username and request.form['password'] == password:
            session['admin_logged_in'] = True
            return redirect('/api/admin_dashboard')
        else:
            return render_template('admin_login.html', error='Invalid username or password')
    return render_template('admin_login.html')

@admin_blueprint.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/api/admin_login')

@admin_blueprint.route('/admin_dashboard')
@admin_login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')