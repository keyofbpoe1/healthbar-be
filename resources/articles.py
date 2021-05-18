# this is our users route!!!
import models

from flask import Blueprint, jsonify, request

# playhouse.shortcuts has a lot of useful peewee tools
from playhouse.shortcuts import model_to_dict

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
articles = Blueprint('articles', 'article')

# get articles route
@articles.route('/', methods=["GET"])
def get_all_articles():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        articles = [model_to_dict(article) for article in models.Article.select()]
        print(articles)
        return jsonify(data=articles, status={"code": 200, "message": "Success articles"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# show a user route
# @users.route('/<id>', methods=["GET"])
# def get_one_user(id):
#     print(id, 'reserved word?')
#     user = models.User.get_by_id(id)
#     print(user.__dict__)
#     return jsonify(
#         data=model_to_dict(user),
#         status= 200,
#         message="Success single"
#     ), 200

# post a new articles route!
@articles.route('/', methods=["POST"])
def create_articles():
    ## see request payload anagolous to req.body in express
    # plus turning it into json
    payload = request.get_json()
    print(type(payload), 'payload')
    article = models.Article.create(**payload)
    ## see the object
    # print(article.__dict__)
    ## Look at all the methods
    # print(dir(article))
    # Change the model to a dict
    print(model_to_dict(article), 'model to dict')
    article_dict = model_to_dict(article)
    return jsonify(data=article_dict, status={"code": 201, "message": "Success"}), 201
#
# # update a user route
# @users.route('/<id>', methods=["PUT"])
# def update_user(id):
#     payload = request.get_json()
#     query = models.User.update(**payload).where(models.User.id==id)
#     query.execute()
#     return jsonify(
#         data=model_to_dict(models.User.get_by_id(id)),
#         status=200,
#         message= 'User updated successfully'
#     ), 200
#
# # delete route!
# @users.route('/<id>', methods=["Delete"])
# def delete_user(id):
#     query = models.User.delete().where(models.User.id==id)
#     query.execute()
#     return jsonify(
#         data='User successfully deleted',
#         message= 'User deleted successfully',
#         status=200
#     ), 200
