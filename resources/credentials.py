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

# post a new credential route!
@credentials.route('/', methods=["POST"])
@login_required
def create_credential():
    """create and post a new credential"""
    # get payload
    payload = request.get_json()
    # set user
    # payload['user'] = current_user
    # create cred in db
    credential = models.Credential.create(**payload)
    credential_dict = model_to_dict(credential)
    return jsonify(data=credential_dict, status={"code": 201, "message": "Credential Post Success"}), 201

# delete a cred route
@credentials.route('/<id>', methods=["DELETE"])
@login_required
def delete_credential(id):
    """if user is authorized, delete cred"""
    # get and check cred author against current_user
    the_credential = models.Credential.get_by_id(id)
    if current_user.id == the_credential.user.id or current_user.role == 'admin':
        # delete cred
        query = models.Credential.delete().where(models.Credential.id==id)
        query.execute()
        return jsonify(
            data='Credential successfully deleted',
            status={"code": 200, "message": "Credential deleted successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
