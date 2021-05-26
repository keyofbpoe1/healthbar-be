# this is our users route!!!
import models
import sys
import os

from flask import Blueprint, jsonify, request, Flask, flash, redirect, url_for, session, send_from_directory, send_file, safe_join
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_manager, login_required
from werkzeug.utils import secure_filename
from os.path import join, dirname

# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
uploads = Blueprint('uploads', 'upload')

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @uploads.route('/post', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(uploads.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return "uploaded"

# post new upload
@uploads.route('/upload/<folder>/<fname>', methods=['POST'])
def fileUpload(folder, fname):
    # target=os.path.join(UPLOAD_FOLDER)
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    # logger.info("welcome to upload`")
    file = request.files['file']
    split_tup = os.path.splitext(file.filename)
    filename = secure_filename(fname)
    # destination="/".join([target, filename])
    destination=os.path.join(f'uploads/{folder}', f'{filename}{split_tup[1]}')
    # print(destination)
    # print(destination, file=sys.stderr)
    # print(destination, file=sys.stdout)
    file.save(destination)
    session['uploadFilePath']=destination
    # response=jsonify(
    #     file=send_from_directory('uploads', filename),
    #     # url_for('fileUpload'),
    #     path=session['uploadFilePath'],
    #     status={"code": 200, "message": "Upload successfull"}
    # ), 200
    return send_from_directory(f'uploads/{folder}', f'{filename}{split_tup[1]}')

#get uploaded file
@uploads.route('/upload/<folder>/<file>', methods=['GET'])
def file_get(folder, file):
    # target=os.path.join(UPLOAD_FOLDER)
    # if not os.path.isdir(target):
    #     os.mkdir(target)

    # logger.info("welcome to upload`")
    # file = request.files['file']
    # filename = secure_filename(file.filename)
    # # destination="/".join([target, filename])
    # destination=os.path.join('uploads', filename)
    # # print(destination)
    # # print(destination, file=sys.stderr)
    # # print(destination, file=sys.stdout)
    # file.save(destination)
    # session['uploadFilePath']=destination
    # response=jsonify(
    #     file=send_from_directory('uploads', filename),
    #     # url_for('fileUpload'),
    #     path=session['uploadFilePath'],
    #     status={"code": 200, "message": "Upload successfull"}
    # ), 200
    return send_from_directory(f'uploads/{folder}', file)


# get discussions route
# @discussions.route('/', methods=["GET"])
# def get_all_discussions():
#     ## find all the discussions and change each one to a dictionary into a new array
#     try:
#         discussions = [model_to_dict(discussion) for discussion in models.Discussion.select()]
#         print(discussions)
#         return jsonify(data=discussions, status={"code": 200, "message": "Success discussions"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 200
#
# # show a single discussion route
# @discussions.route('/<id>', methods=["GET"])
# def get_one_discussion(id):
#     """get and return a single discussion"""
#     discussion = models.Discussion.get_by_id(id)
#     return jsonify(
#         data=model_to_dict(discussion),
#         status={"code": 200, "message": "Success single discussion"}
#     ), 200
#
# # post a new discussion route!
# @discussions.route('/', methods=["POST"])
# @login_required
# def create_discussion():
#     """create and post a new discussion"""
#     # get payload
#     payload = request.get_json()
#     # print(payload, file=sys.stderr)
#     # print(payload, file=sys.stdout)
#     # set author
#     payload['author'] = current_user
#     # create discussion in db
#     discussion = models.Discussion.create(**payload)
#     discussion_dict = model_to_dict(discussion)
#     return jsonify(data=discussion_dict, status={"code": 201, "message": "Discussion Post Success"}), 201
#
# # update a discussion route
# @discussions.route('/<id>', methods=["PUT"])
# @login_required
# def update_discussions(id):
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
# # delete an article route
# @discussions.route('/<id>', methods=["DELETE"])
# @login_required
# def delete_discussion(id):
#     """if user is authorized, delete discussion"""
#     # get and check discussion author against current_user
#     the_discussion = models.Discussion.get_by_id(id)
#     if current_user.id == the_discussion.author.id or current_user.role == 'admin':
#         # delete article
#         query = models.Discussion.delete().where(models.Discussion.id==id)
#         query.execute()
#         return jsonify(
#             data='Discussion successfully deleted',
#             status={"code": 200, "message": "Discussion deleted successfully"}
#         ), 200
#     else:
#         return jsonify(data={}, status={"code": 403, "message": "Not authorized"})
