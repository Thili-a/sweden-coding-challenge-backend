from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "logged in", 200