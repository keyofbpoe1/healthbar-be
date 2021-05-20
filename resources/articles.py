# this is our users route!!!
import models
import sys

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_manager, login_required

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
articles = Blueprint('articles', 'article')

# get articles route
@articles.route('/', methods=["GET"])
def get_all_articles():
    ## find all the articles and change each one to a dictionary into a new array
    try:
        articles = [model_to_dict(article) for article in models.Article.select()]
        print(articles)
        return jsonify(data=articles, status={"code": 200, "message": "Success articles"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# search articles route
@articles.route('/search/<term>/<page>/<limit>', methods=["GET"])
def search_articles(term, page, limit):
    ## find all the articles containing our query and change each one to a dictionary into a new array
    try:
        articles = models.Article.select().join(models.User).where(
            (models.Article.title ** f'%{term}%') |
            (models.Article.title ** f'*{term}*') |
            (models.Article.body ** f'%{term}%') |
            (models.Article.body ** f'*{term}*') |
            (models.Article.category ** f'%{term}%') |
            (models.Article.category ** f'*{term}*') |
            (models.Article.author.username ** f'%{term}%') |
            (models.Article.author.username ** f'*{term}*') |
            (models.Article.author.email ** f'%{term}%') |
            (models.Article.author.email ** f'*{term}*')
        )


        # [model_to_dict(article) for article in models.Article.select().join(models.User).where(
        #     (models.Article.title ** f'%{term}%') |
        #     (models.Article.title ** f'*{term}*') |
        #     (models.Article.body ** f'%{term}%') |
        #     (models.Article.body ** f'*{term}*') |
        #     (models.Article.category ** f'%{term}%') |
        #     (models.Article.category ** f'*{term}*') |
        #     (models.Article.author.username ** f'%{term}%') |
        #     (models.Article.author.username ** f'*{term}*') |
        #     (models.Article.author.email ** f'%{term}%') |
        #     (models.Article.author.email ** f'*{term}*')
        # )]

        page_articles = [model_to_dict(article) for article in articles.paginate(int(page), int(limit))]
        return jsonify(data=page_articles, artlength=articles.count(), status={"code": 200, "message": "Success search articles"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# show a single article route
@articles.route('/<id>', methods=["GET"])
def get_one_article(id):
    # get article
    article = models.Article.get_by_id(id)
    # get related discussion
    discussions = [model_to_dict(discussion) for discussion in article.discussions]
    return jsonify(
        data=model_to_dict(article),
        discussions=discussions,
        status={"code": 200, "message": "Success single article"}
    ), 200

# post a new articles route!
@articles.route('/', methods=["POST"])
@login_required
def create_article():
    """create and post a new article"""
    # get payload
    payload = request.get_json()
    # set author
    payload['author'] = current_user
    # create article in db
    article = models.Article.create(**payload)
    article_dict = model_to_dict(article)
    return jsonify(data=article_dict, status={"code": 201, "message": "Article Post Success"}), 201

# update an article route
@articles.route('/<id>', methods=["PUT"])
@login_required
def update_article(id):
    """if user is authorized, update article"""
    # get and check article author against current_user
    the_article = models.Article.get_by_id(id)
    if current_user.id == the_article.author.id or current_user.role == 'admin':
        # get payload
        payload = request.get_json()
        # run update
        query = models.Article.update(**payload).where(models.Article.id==id)
        query.execute()
        return jsonify(
            data=model_to_dict(models.Article.get_by_id(id)),
            status={"code": 200, "message": "Article updated successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})

# delete an article route
@articles.route('/<id>', methods=["DELETE"])
@login_required
def delete_article(id):
    """if user is authorized, delete article"""
    # get and check article author against current_user
    the_article = models.Article.get_by_id(id)
    if current_user.id == the_article.author.id or current_user.role == 'admin':
        # delete article
        query = models.Article.delete().where(models.Article.id==id)
        query.execute()
        return jsonify(
            data='Article successfully deleted',
            status={"code": 200, "message": "Article deleted successfully"}
        ), 200
    else:
        return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
