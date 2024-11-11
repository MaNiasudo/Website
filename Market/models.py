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

    user = db.relationship("User", back_populates="notes")

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True,nullable=False)
    password = db.Column(db.String(355),nullable=False)
    first_name = db.Column(db.String(150),nullable=False)
    budget = db.Column(db.Integer(),nullable=False, default=10000)

    items = db.relationship("Item", back_populates="user", lazy=True)
    notes = db.relationship("Note", back_populates="user", lazy=True)

    def __init__(self,email , first_name , password=None):
        self.email = email 
        self.first_name = first_name
        if password :
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)




class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price  = db.Column(db.Integer(), nullable=False )
    barcode  = db.Column(db.String(length=12), nullable=False , unique=True)
    description  = db.Column(db.String(length=350), nullable=False , unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="items")

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer(),primary_key=True)
    tasktext = db.Column(db.String(length=250), nullable=False)
