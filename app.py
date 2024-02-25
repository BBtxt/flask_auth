from flask import Flask, redirect, render_template, request
from models import db, connect_db
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh. its a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()