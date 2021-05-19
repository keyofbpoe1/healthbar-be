# this is our users route!!!
import models
import sys

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_manager, login_required

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
discussions = Blueprint('discussions', 'discussion')

# get articles route
@discussions.route('/', methods=["GET"])
def get_all_discussions():
    ## find all the discussions and change each one to a dictionary into a new array
    try:
        discussions = [model_to_dict(discussion) for discussion in models.Discussion.select()]
        print(discussions)
        return jsonify(data=discussions, status={"code": 200, "message": "Success discussions"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# show a sigle article route
@discussions.route('/<id>', methods=["GET"])
def get_one_discussion(id):
    """get and return a single discussion"""
    discussion = models.Discussion.get_by_id(id)
    return jsonify(
        data=model_to_dict(discussion),
        status={"code": 200, "message": "Success single discussion"}
    ), 200

# post a new discussion route!
@discussions.route('/', methods=["POST"])
@login_required
def create_discussion():
    """create and post a new discussion"""
    # get payload
    payload = request.get_json()
    # set author
    payload['author'] = current_user
    # create discussion in db
    discussion = models.Discussion.create(**payload)
    discussion_dict = model_to_dict(discussion)
    return jsonify(data=discussion_dict, status={"code": 201, "message": "Discussion Post Success"}), 201

# update a discussion route
@discussions.route('/<id>', methods=["PUT"])
@login_required
def update_discussions(id):
    """if user is authorized, update discussion"""
    # get and check discussion author against current_user
    the_discussion = models.Discussion.get_by_id(id)
    if not current_user.id == the_discussion.author.id or current_user.role == 'admin':
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
    else:
        # get payload
        payload = request.get_json()
        # run update
        query = models.Discussion.update(**payload).where(models.Discussion.id==id)
        query.execute()
        return jsonify(
            data=model_to_dict(models.Discussion.get_by_id(id)),
            status={"code": 200, "message": "Discussion updated successfully"}
        ), 200

# delete an article route
@discussions.route('/<id>', methods=["DELETE"])
@login_required
def delete_discussion(id):
    """if user is authorized, delete discussion"""
    # get and check discussion author against current_user
    the_discussion = models.Discussion.get_by_id(id)
    if not current_user.id == the_discussion.author.id or current_user.role == 'admin':
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
    else:
        # delete article
        query = models.Discussion.delete().where(models.Discussion.id==id)
        query.execute()
        return jsonify(
            data='Discussion successfully deleted',
            status={"code": 200, "message": "Discussion deleted successfully"}
        ), 200
