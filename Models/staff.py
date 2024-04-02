from app import db

class Staff(db.Model):
    __tablename__ = 'Staffs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    tel = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date_of_employment = db.Column(db.Date, nullable=False)
    

    def __repr__(self):
        return f'<Staff {self.name}>'

