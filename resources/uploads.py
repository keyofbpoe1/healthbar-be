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

# post new upload
@uploads.route('/upload', methods=['GET', 'POST'])
def fileUpload():

    if request.method == 'POST':

        file = request.files['file']
        folder = request.form.get('folder')
        fname = request.form.get('fname')

        filename = secure_filename(fname)

        destination=os.path.join(f'uploads/{folder}', f'{filename}')

        file.save(destination)
        session['uploadFilePath']=destination


        # response=jsonify(
        #     file=send_from_directory(f'uploads/{folder}', f'{filename}'),
        #     status={"code": 200, "message": "Upload successfull"}
        # ), 200
        response=send_from_directory(f'uploads/{folder}', f'{filename}')
        return response

    else:
        folder = request.headers['folder']
        fname = request.headers['fname']
        response=send_from_directory(f'uploads/{folder}', f'{fname}')
        return response

# #get uploaded file
# @uploads.route('/upload/<folder>/<file>', methods=['GET'])
# def file_get(folder, file):
#     # target=os.path.join(UPLOAD_FOLDER)
#     # if not os.path.isdir(target):
#     #     os.mkdir(target)
#
#     # logger.info("welcome to upload`")
#     # file = request.files['file']
#     # filename = secure_filename(file.filename)
#     # # destination="/".join([target, filename])
#     # destination=os.path.join('uploads', filename)
#     # # print(destination)
#     # # print(destination, file=sys.stderr)
#     # # print(destination, file=sys.stdout)
#     # file.save(destination)
#     # session['uploadFilePath']=destination
#     # response=jsonify(
#     #     file=send_from_directory('uploads', filename),
#     #     # url_for('fileUpload'),
#     #     path=session['uploadFilePath'],
#     #     status={"code": 200, "message": "Upload successfull"}
#     # ), 200
#     return send_from_directory(f'uploads/{folder}', file)
