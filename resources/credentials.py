# this is our users route!!!
import models
import sys

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_manager, login_required

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
credentials = Blueprint('credentials', 'credential')

# get discussions route
# @credentials.route('/', methods=["GET"])
# def get_all_credentials():
#     ## find all the credentials and change each one to a dictionary into a new array
#     try:
#         discussions = [model_to_dict(discussion) for discussion in models.Discussion.select()]
#         print(discussions)
#         return jsonify(data=discussions, status={"code": 200, "message": "Success discussions"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200
#
# # show a single discussion route
# @credentials.route('/<id>', methods=["GET"])
# def get_one_credential(id):
#     """get and return a single credential"""
#     credential = models.Discussion.get_by_id(id)
#     return jsonify(
#         data=model_to_dict(credential),
#         status={"code": 200, "message": "Success single credential"}
#     ), 200

# post a new credential route!
@credentials.route('/', methods=["POST"])
@login_required
def create_credential():
    """create and post a new credential"""
    # get payload
    payload = request.get_json()
    # set user
    # payload['user'] = current_user
    # create discussion in db
    credential = models.Credential.create(**payload)
    credential_dict = model_to_dict(credential)
    return jsonify(data=credential_dict, status={"code": 201, "message": "Credential Post Success"}), 201

# update a discussion route
# @credentials.route('/<id>', methods=["PUT"])
# @login_required
# def update_credentials(id):
#     """if user is authorized, update discussion"""
#     # get and check discussion author against current_user
#     the_discussion = models.Discussion.get_by_id(id)
#     if current_user.id == the_discussion.author.id or current_user.role == 'admin':
#         # get payload
#         payload = request.get_json()
#         # run update
#         query = models.Discussion.update(**payload).where(models.Discussion.id==id)
#         query.execute()
#         return jsonify(
#             data=model_to_dict(models.Discussion.get_by_id(id)),
#             status={"code": 200, "message": "Discussion updated successfully"}
#         ), 200
#     else:
#         return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
#
# delete a cred route
@credentials.route('/<id>', methods=["DELETE"])
@login_required
def delete_credential(id):
    """if user is authorized, delete discussion"""
    # get and check discussion author against current_user
    the_credential = models.Credential.get_by_id(id)
    if current_user.id == the_credential.user.id or current_user.role == 'admin':
        # delete article
        query = models.Credential.delete().where(models.Credential.id==id)
        query.execute()
        return jsonify(
            data='Credential successfully deleted',
            status={"code": 200, "message": "Credential deleted successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
