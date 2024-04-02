from app import db

class LoginModel(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def authenticate(self, username, password):
        return LoginModel.query.filter_by(username=username, password=password).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = LoginModel().authenticate(username, password)

        if admin:
            session['admin_id'] = admin.id
            return redirect('/admin_dashboard')
        else:
            return render_template('admin_login.html', error='Invalid username or password')
    
    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def dashboard():
    if 'admin_id' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect('/admin_login')


@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect('/admin_login')
