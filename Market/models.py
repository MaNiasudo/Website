from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash , check_password_hash
import re

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))    
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref="notes")

class UserFamilies(db.Model):
    __tablename__ = 'user_families'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    family_id = db.Column('family_id', db.Integer, db.ForeignKey('family.id'))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True,nullable=False)
    password = db.Column(db.String(355),nullable=False)
    username = db.Column(db.String(150),unique=True,nullable=False)
    budget = db.Column(db.Integer(),nullable=False, default=10000)
    
    families = db.relationship('Family', secondary='user_families', backref='users')
  
    
    def __init__(self,email , first_name , password=None):
        self.email = email 
        self.first_name = first_name
        if password :
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Family(db.Model):
    __tablename__ = "family"
    id = db.Column(db.Integer(),primary_key=True)
    family_name = db.Column(db.String(length=200), nullable=False)

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price  = db.Column(db.Integer(), nullable=False )
    barcode  = db.Column(db.String(length=12), nullable=False , unique=True)
    description  = db.Column(db.String(length=350), nullable=False , unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", backref="items")

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer(), primary_key=True)
    task_text = db.Column(db.String(length=250), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    # Relationships
    user = db.relationship('User', backref='tasks')  # Access user's tasks
    family = db.relationship('Family', backref='tasks')  # Access family's tasks

    def __repr__(self):
        return f'<Task {self.task_text}>'


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    read = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # Relationships
    user = db.relationship('User', backref='notifications')
    task = db.relationship('Task', backref='notifications')

    def __repr__(self):
        return f'<Notification {self.message}>'

    
