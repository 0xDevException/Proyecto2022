from flask import url_for
from flask_login import UserMixin
#from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from run import db, app

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    country = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    cargo = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "country": self.country,
                "city": self.city,
                "phone": self.phone,
                "cargo": self.cargo,
                "is_admin": self.is_admin}

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()


    
    @staticmethod
    def get_all():
        return User.query.all()

class SensorData(db.Model):
    __tablename__ = 'sensorData'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    value1 = db.Column(db.String(128), nullable=False)
    value2 = db.Column(db.String(128), nullable=False)
    value3 = db.Column(db.String(128), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "location": self.location,
                "value1": self.value1,
                "value2": self.value2,
                "value3": self.value3}

    @staticmethod
    def get_all(id):
        return SensorData.query.filter_by(admin_id=id).all()
    
    @staticmethod
    def get_last(id):
        return SensorData.query.filter_by(admin_id=id).order_by(SensorData.id.desc()).first()

    @staticmethod
    def get_first():
        return SensorData.query.first()

    @staticmethod
    def get_lastTwo(id):
        return SensorData.query.filter_by(admin_id=id).order_by(SensorData.id).limit(7) #Probar este metodo

class TaskData(db.Model):
    __tablename__ = 'taskData'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    task = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "task": self.task,
                "status": self.status}
    
    @staticmethod
    def get_all_admin(id):
        return TaskData.query.filter_by(admin_id=id).all()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_user(id):
        return TaskData.query.filter_by(user_id=id).all()
    
    @staticmethod
    def delete_task(id):
        return TaskData.query.filter_by(user_id=id).first()

with app.app_context():
     db.create_all()  