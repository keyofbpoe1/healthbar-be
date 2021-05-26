# this is our server!

# import flask framework
from flask import Flask, jsonify, after_this_request, g, request, flash, redirect, url_for, session
# import env vars
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# run to actually import vars from file
# load_dotenv()
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import models
from resources.users import users
from resources.articles import articles
from resources.discussions import discussions
# from resources.uploads import uploads

# cors allow for our db port
# CORS(dog, origins=[os.environ.get("ORIGIN")], supports_credentials=True)

# set consts
DEBUG = True # for verbose error msgs
PORT = os.environ.get("PORT") # our port, of course

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

CORS(app, origins=[os.environ.get("ORIGIN")], supports_credentials=True)

# 1. set up a secret/key for sessions
# as demonstrated here: https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
app.secret_key = os.environ.get("SECRET")

# 2. instantiate the LoginManager to actually get a login_manager
login_manager = LoginManager()

# 3. actually connect the app with the login_manager
login_manager.init_app(app)

# 4. load current_user from the user id store in the session
@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)

# connect and disconnect db
# @app.before_request # use this decorator to cause a function to run before reqs
# def before_request():
#
#     """Connect to the db before each request"""
#     print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
#     models.DATABASE.connect()
#
#     @after_this_request # use this decorator to Executes a function after this request
#     def after_request(response):
#         """Close the db connetion after each request"""
#         print("you should see this after each request") # optional -- to illustrate that this code runs after each request
#         models.DATABASE.close()
#         return response # go ahead and send response back to client
                      # (in our case this will be some JSON)
# @app.before_request
# def before_request():
#     """Connect to the database before each request."""
#     g.db = models.DATABASE
#     g.db.connect()
#
#
# @app.after_request
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)

    # logger.info("welcome to upload`")
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    # print(destination)
    # print(destination, file=sys.stderr)
    # print(destination, file=sys.stdout)
    file.save(destination)
    session['uploadFilePath']=destination
    response=jsonify(
        session=session,
        status={"code": 200, "message": "Whatever you wish too return"}
    ), 200
    return response

# cors for our routes
CORS(users, origins=[os.environ.get("ORIGIN")], supports_credentials=True)
CORS(articles, origins=[os.environ.get("ORIGIN")], supports_credentials=True)
CORS(discussions, origins=[os.environ.get("ORIGIN")], supports_credentials=True)
# CORS(uploads, origins=[os.environ.get("ORIGIN")], supports_credentials=True)

# get our api on!
# this hooks up to our router
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(articles, url_prefix='/api/v1/articles')
app.register_blueprint(discussions, url_prefix='/api/v1/discussions')
# app.register_blueprint(uploads, url_prefix='/api/v1/uploads')

# The default URL ends in / ("my-website.com/").
# @app.route('/')
# def index():
#     return 'hi'

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
    print('\non heroku!')
    models.initialize()
