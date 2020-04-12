from config import Config
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from functools import wraps
from util import *
import csv
import datetime
import jwt
import pandas as pd
import pymongo
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import pandas as pd
from ml_backend.Pipeline import Pipeline


app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = Config.MONGO_URI
mongodb = PyMongo(app)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Token']

        if not token:
            return jsonify({'message': 'Token is missing !'}), 403

        try:
            data = jwt.decode(token, Config.TOKEN_SECRET_KEY)
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)
    return decorated


@app.route("/")
def hello():
    return jsonify({"about": "hello world"})

@app.route("/login", methods=['POST'])
def login():
    username = request.get_json(force = True)['username']
    password = request.get_json(force = True)['password']

    users = mongodb.db.users
    if users.find_one({'username': username, 'password': password}):

        # generate token
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.TOKEN_SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'error':'Could not verify!', 'WWW-Authenticate': 'Basic realm="Login Required"'}), 401

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        users = mongodb.db.users

        username = request.get_json(force = True)['username']
        password = request.get_json(force = True)['password']
        firstname = request.get_json(force = True)['firstname']
        lastname = request.get_json(force = True)['lastname']


        existing_user = users.find_one({'username':  username})

        if existing_user is None:
            users.insert({
                'username': username,
                'password': password,
                'firstname': firstname,
                'lastname': lastname
            })
            return jsonify({'message':'sign up sucessfully'})

        return jsonify({'error': 'username existed'}), 422
    else:
        return''


@app.route("/userinfo", methods=['POST'])
def user():
    username = request.get_json(force = True)['username']

    users = mongodb.db.users
    user = users.find_one({'username': username})
    return jsonify({
        'firstname': user['firstname'],
        'lastname': user['lastname'],
    })

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        print(request.files)
        return resp
    files = request.files.getlist('files[]')
    details = request.form.get('details')
    time = request.form.get('time')
    print(files)
    names = []
    sizes = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            names.append(filename)
            size = len(file.read())
            sizes.append(size)
    print(files)
    print(names)
    print(sizes)
    print(time)
    print(details)
    result = Pipeline.run_MLAI(files, names, sizes, None, None, None, {'time': time, 'userid': '111111', 'user_input': details})   
    print(result)
            
    resp = jsonify({'message' : 'File successfully uploaded'})
    resp.status_code = 201
    return resp

@app.route("/developerfeedback", methods=['POST'])
def developer_feedback():
    email_address = request.get_json(force = True)['email_address']
    name = request.get_json(force = True)['name']
    feedback = request.get_json(force = True)['feedback']
    subject = request.get_json(force = True)['subject']

    return send_feedback_email(email_address, name, feedback, subject)


@app.route("/dev/register", methods=['POST'])
def developer_register():
    if request.method == 'POST':
        devs = mongodb.db.devs

        devname = request.get_json(force=True)['devname']
        password = request.get_json(force = True)['password']
        firstname = request.get_json(force = True)['firstname']
        lastname = request.get_json(force = True)['lastname']


        existing_dev = devs.find_one({'devname':  devname})

        if existing_dev is None:
            devs.insert({
                'devname': username,
                'password': password,
                'firstname': firstname,
                'lastname': lastname
            })
            return jsonify({'message':'sign up sucessfully'})

        return jsonify({'error': 'developer existed'}), 422
    else:
        return ''

@app.route("/dev/login", methods=['POST'])
def dev_login():
    devname = request.get_json(force = True)['devname']
    password = request.get_json(force = True)['password']

    devs = mongodb.db.devs
    if devs.find_one({'devname': devname, 'password': password}):

        # generate token
        token = jwt.encode({'dev': devname, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.TOKEN_SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'error':'Could not verify!', 'WWW-Authenticate': 'Basic realm="Login Required"'}), 401



def save_upload(f):
    mongodb.save_file(f.filename, f, 'data')
    return get_upload(f.filename)

def get_upload(filename):
    return mongodb.send_file(filename)

@app.route('/protected', methods=['POST'])
@token_required
def protected():
    return jsonify({'message': 'with token'})

#was only used to test send_json_to_database, will be deleted in a future commit
# @app.route("/pythonobject", methods=['POST'])
# def python_object():
#     username = request.get_json(force = True)['username']
#
#     return send_json_to_database(username, {"a": 3})

if __name__ == '__main__':
    app.run(debug=True)
