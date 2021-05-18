# this is our server!

# import flask framework
from flask import Flask, jsonify, g
# import env vars
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask_cors import CORS

# run to actually import vars from file
# load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import models
from resources.users import users
from resources.articles import articles

# cors allow for our db port
# CORS(dog, origins=[os.environ.get("ORIGIN")], supports_credentials=True)

# set consts
DEBUG = True # for verbose error msgs
PORT = os.environ.get("PORT") # our port, of course

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

# connect and disconnect db
@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

# get our api on!
# this hooks up to our router
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(articles, url_prefix='/api/v1/articles')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
