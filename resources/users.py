# this is our users route!!!
import models
import sys

from flask import Blueprint, jsonify, request, session
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user, current_user, login_manager, login_required

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
users = Blueprint('users', 'user')

# get users route
@users.route('/', methods=["GET"])
def get_all_users():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# search users route
@users.route('/search/<term>', methods=["GET"])
def search_users(term):
    ## find all the users containing our query and change each one to a dictionary into a new array
    try:
        users = [model_to_dict(user) for user in models.User.select().where(
            (models.User.username ** f'%{term}%') |
            (models.User.username ** f'*{term}*') |
            (models.User.email ** f'%{term}%') |
            (models.User.email ** f'*{term}*')
        )]
        return jsonify(data=users, status={"code": 200, "message": "Success search users"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200
#

#
# # post a new user route!
# @users.route('/', methods=["POST"])
# def create_users():
#     ## see request payload anagolous to req.body in express
#     # plus turning it into json
#     payload = request.get_json()
#     print(type(payload), 'payload')
#     user = models.User.create(**payload)
#     ## see the object
#     # print(user.__dict__)
#     ## Look at all the methods
#     # print(dir(user))
#     # Change the model to a dict
#     print(model_to_dict(user), 'model to dict')
#     user_dict = model_to_dict(user)
#     return jsonify(data=user_dict, status={"code": 201, "message": "Success"}), 201
#

#


# show a user route
@users.route('/<id>', methods=["GET"])
def get_one_user(id):
    # get user
    user = models.User.get_by_id(id)
    #  get user's articles
    articles = [model_to_dict(article) for article in user.articles]
    return jsonify(
        data=model_to_dict(user),
        articles=articles,
        status={"code": 200, "message": "Success single user"}
    ), 200

# update a user route
@users.route('/<id>', methods=["PUT"])
@login_required
def update_user(id):
    """if user is authorized, update user"""
    # get and check user
    # print(current_user.role, file=sys.stderr)
    # print(current_user.role, file=sys.stdout)
    the_user = models.User.get_by_id(id)
    if current_user.id == the_user.id or current_user.role == 'admin':
    # if not current_user.role == 'admin':
        payload = request.get_json()
        # turn it all lowercase
        payload['email'] = payload['email'].lower()
        payload['username'] = payload['username'].lower()
        # run update
        query = models.User.update(**payload).where(models.User.id==id)
        query.execute()
        return jsonify(
            data=model_to_dict(models.User.get_by_id(id)),
            status={"code": 200, "message": "User updated successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})

# register route
@users.route('/register', methods=["POST"])
def register():
    """register and login a new user"""
    # get payload json
    payload = request.get_json()
    # turn it all lowercase
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    # set role to user
    payload['role'] = 'user'

    try:
        # Find if the username already exists?
        models.User.get(models.User.username == payload['username'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that username already exists"})
    except models.DoesNotExist:
        try:
            # Find if the user email already exists?
            models.User.get(models.User.email == payload['email'])
            return jsonify(data={}, status={"code": 401, "message": "A user with that email already exists"})
        except models.DoesNotExist:
            # if all good
            # bcrypt hash the password
            payload['password'] = generate_password_hash(payload['password'])
            # create user
            user = models.User.create(**payload)

            # start user session
            login_user(user)
            user_dict = model_to_dict(user)
            # delete the password before we return it, because we don't need the client to be aware of it
            del user_dict['password']
            return jsonify(data=user_dict, status={"code": 201, "message": " Registration Success"})

# login route
@users.route('/login', methods=["POST"])
def login():
    """check user credentials and create session"""
    # get payload json
    payload = request.get_json()
    # all to lowercase
    # payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    try:
        # try to find user
        user = models.User.get(models.User.username == payload['username'])
        # if you find the User model convert in to a dictionary so you can edit and jsonify it
        user_dict = model_to_dict(user)
        # check bcrypt hash password
        if(check_password_hash(user_dict['password'], payload['password'])):
            # delete the password since the client doesn't need it
            del user_dict['password']
            # set up the session
            login_user(user)
            # return success response
            return jsonify(data=user_dict, status={"code": 200, "message": "Login Success"})
        else:
            # return fail response
            return jsonify(data={}, status={"code": 401, "message": "Username or password incorrect"})
    except models.DoesNotExist:
        # return fail response
        return jsonify(data={}, status={"code": 401, "message": "Username or password incorrect"})

#logout route
@users.route('/logout', methods=["GET"])
def logout():
    """end current session"""
    logout_user()
    # return response
    return jsonify(data={}, status={"code": 200, "message": "Logout Success"})

# check logged in route
@users.route('/checksession', methods=["GET"])
@login_required
def checksession():
    """check if current user is logged in"""
    # user_id = session
    # print(user_id, file=sys.stderr)
    # print(user_id, file=sys.stdout)
    # return user details
    return jsonify(data={}, status={"code": 200, "message": "Login Check Success"}, curus={"id": current_user.id, "username": current_user.username, "email": current_user.email, "role": current_user.role})

# delete route!
@users.route('/<id>', methods=["Delete"])
@login_required
def delete_user(id):
    """if user is authorized, delete user"""
    # get and check user
    the_user = models.User.get_by_id(id)
    if current_user.id == the_user.id or current_user.role == 'admin':
        # delete user
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        logout_user()
        return jsonify(
            data='User successfully deleted',
            status={"code": 200, "message": "User deleted successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
