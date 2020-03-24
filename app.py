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


app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = Config.MONGO_URI
mongodb = PyMongo(app)

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


@app.route("/upload", methods=['POST'])
def upload():
    if len(request.files) != 0:
        f = request.files['file']
        fstring = f.read()

        # using csv reader
        csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.decode().splitlines(), skipinitialspace=True)]

        # for d in csv_dicts:
        #     for x, y in d.items():
        #         print(x, y)
        #     print("----------------------------")

        # using panda

        df = pd.read_csv(StringIO(fstring.decode()), delimiter='\n').T.to_dict()


    return jsonify({
        "message": "accepted file"
    })

@app.route("/developerfeedback", methods=['POST'])
def developer_feedback():
    email_address = request.get_json(force = True)['email_address']
    name = request.get_json(force = True)['name']
    feedback = request.get_json(force = True)['feedback']
    subject = request.get_json(force = True)['subject']

    return send_feedback_email(email_address, name, feedback, subject)

def save_upload(f):
    mongodb.save_file(f.filename, f, 'data')
    return get_upload(f.filename)

def get_upload(filename):
    return mongodb.send_file(filename)

@app.route('/protected', methods=['POST'])
@token_required
def protected():
    return jsonify({'message': 'with token'})


if __name__ == '__main__':
    app.run(debug=True)
