import sys
from flask import render_template, redirect, url_for, request, abort

from models.User import User

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def index():
    return {"home": "this is the home route"}

def store():
    ...

def show(userId):
    ...

def update(userId):
    ...

def delete(userId):
    ...