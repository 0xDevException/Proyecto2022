import sys
from flask import render_template, redirect, url_for, request, abort

from models.User import User

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def index():
    return render_template('users.html')

def store():
    ...

def show(userId):
    ...

def create():
    if not request.json:
        abort(400)
    user = User(
        name=request.json.get('name'),
        city=request.json.get('city'),
        state=request.json.get('state'),
        address=request.json.get('address')
    )
    db.session.add(user)
    db.session.commit()

def update(userId):
    if not request.json:
        abort(400)
    user = User.query.get(userId)
    if user is None:
        abort(404)
    user.name = request.json.get('name', user.name)
    user.city = request.json.get('city', user.city)
    user.state = request.json.get('state', user.state)
    user.address = request.json.get('address', user.address)
    db.session.commit()

def delete(userId):
    user = User.query.get(userId)
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()