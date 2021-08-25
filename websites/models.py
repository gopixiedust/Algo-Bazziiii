from sqlalchemy.orm import query
from . import db
from flask_login import UserMixin
from sqlalchemy import func
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    cards = db.relationship('Card', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query=db.Column(db.String(64))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))