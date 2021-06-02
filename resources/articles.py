# this is our users route!!!
import models
import sys
import json

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_manager, login_required

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
articles = Blueprint('articles', 'article')

# get articles route
@articles.route('/allarticles/<page>/<limit>', methods=["GET"])
def get_all_articles(page, limit):
    ## find all the articles and change each one to a dictionary into a new array paginate by 10 and sort by id descending
    try:
        articles = models.Article.select()
        page_articles = [model_to_dict(article) for article in articles.paginate(int(page), int(limit)).order_by(models.Article.id.desc())]
        return jsonify(data=page_articles, artlength=articles.count(), status={"code": 200, "message": "Success search articles"})
        return jsonify(data=articles, status={"code": 200, "message": "Success articles"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# get users' articles route
@articles.route('/userarticles/<userid>/<page>/<limit>', methods=["GET"])
def get_user_articles(userid, page, limit):
    ## find all the articles and change each one to a dictionary into a new array paginate by 10 and sort by id descending
    try:
        user = models.User.get_by_id(userid)
        articles = user.articles
        page_articles = [model_to_dict(article) for article in articles.paginate(int(page), int(limit)).order_by(models.Article.id.desc())]
        return jsonify(data=page_articles, artlength=articles.count(), status={"code": 200, "message": "Success search articles"})
        return jsonify(data=articles, status={"code": 200, "message": "Success articles"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200

# search articles route
@articles.route('/search/<page>/<limit>/<term>', methods=["GET"])
def search_articles(term, page, limit):
    ## find all the articles containing our query and change each one to a dictionary into a new array
    t_json = json.loads(term)
    # t_query = t_json['query']
    print(t_json, file=sys.stderr)
    print(t_json, file=sys.stdout)
    try:
        articles = models.Article.select().join(models.User).join(models.Endorsement)

        if t_json['query']:
            articles = articles.select().where(
                (models.Article.title ** f'%{t_json["query"]}%') |
                (models.Article.title ** f'*{t_json["query"]}*') |
                (models.Article.body ** f'%{t_json["query"]}%') |
                (models.Article.body ** f'*{t_json["query"]}*') |
                (models.Article.category ** f'%{t_json["query"]}%') |
                (models.Article.category ** f'*{t_json["query"]}*') |
                (models.Article.author.username ** f'%{t_json["query"]}%') |
                (models.Article.author.username ** f'*{t_json["query"]}*') |
                (models.Article.author.email ** f'%{t_json["query"]}%') |
                (models.Article.author.email ** f'*{t_json["query"]}*')
            )

        if t_json['category']:
            articles = articles.select().where(
                models.Article.category == t_json['category']
            )

        if t_json['endorsements'] and int(t_json['endorsements']) == 1:
            articles = articles.select().where(
                models.Endorsement.article == models.Article.id
            )

        if t_json['endorsements'] and int(t_json['endorsements']) == 0:
            articles = articles.select().where(
                models.Endorsement.article != models.Article.id
            )

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
    endorsements = [model_to_dict(endorsement) for endorsement in article.endorsements]
    return jsonify(
        data=model_to_dict(article),
        discussions=discussions,
        endorsements=endorsements,
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
