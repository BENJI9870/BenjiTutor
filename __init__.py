# imports
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# initialize Flask app
app = Flask(__name__)

# define database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db_user:%40Waterloo6767!@localhost/askthetutor'
db = SQLAlchemy(app)

# set secret key for session. SHOULD BE GIBBERISH
app.secret_key = "as;ldfkjawe;ofiahsdfh;asldkfj"
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)



# create tables in the context of the app
with app.app_context():
    db.create_all()

from AskTheTutor import routes

