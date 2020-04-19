from config import Config
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from functools import wraps
from util import *
import datetime
import jwt
import pymongo
import os
from werkzeug.utils import secure_filename
from ml_backend.Pipeline import Pipeline


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


@app.route("/devuserinfo", methods=['POST'])
def devuser():
    devname = request.get_json(force = true)('Devname');

    devs = mongodb.db.devs
    devs = devs.find_one({'devname': devname})
    return jsonify({
        'firstname': devs['firstname'],
        'lastname': devs['lastname'],
    })

ALLOWED_EXTENSIONS = set(['xlsx', 'pdf', 'png', 'jpg', 'csv'])

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
    print("request.files: " + str(request.files))
    print("request.form: " + str(request.form))

    names = []
    sizes = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            names.append(filename)
            size = len(file.read())
            sizes.append(size)
    result = Pipeline.run_MLAI(files, names, sizes, None, None, None, {'time': time, 'userid': '111111', 'user_input': details})
    print(result)

    resp = jsonify({'message' : 'File successfully uploaded'})
    resp.status_code = 201
    return resp


DEV_ALLOWED_EXTENSIONS = set(['py'])

def dev_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in DEV_ALLOWED_EXTENSIONS

@app.route("/developerfeedback", methods=['POST'])
def developer_feedback():
        # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        print(request.files)
        return resp
    files = request.files.getlist('files[]')
    details = request.form.get('details')
    devname = request.form.get('Devname');
    print("request.files: " + str(request.files))
    print("request.form: " + str(request.form))
    try:
        path = "./ml_backend/devUpload/"

        UPLOAD_FOLDER = path + devname
        os.mkdir(UPLOAD_FOLDER)
    except:
        print ("Directory creation failed (may already be made)")
    else:
        print ("Directory creation successful")

    lastfilename = ""

    for file in files:
        if file and dev_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            lastfilename = file.filename
    lastfilename = lastfilename[:-3]
    f = open(UPLOAD_FOLDER + "/" + lastfilename + ".txt","w+")
    f.write(details)
    f.close()


    resp = jsonify({"message": "Files successfully uploaded"})
    resp.status_code = 201
    return resp
    # #
    # path = "./ml_backend/devUpload/" + devname
    # #
    # ## @Daniel still need to add details to this save
    # try:
    #     os.mkdir(path)
    # except OSError:
    #     print ("Creation of the directory %s failed (likely already created)" % path)
    # else:
    #     print ("Successfully created the directory %s " % path)
    # #
    # for file in files:
    #     if file and dev_allowed_file(file.filename):
    #         filename = file.filename
    #         os.path.join(path,filename)
    # resp = jsonify({'message' : 'File successfully uploaded'})
    # resp.status_code = 201
    # return resp

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
                'devname': devname,
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

@app.route('/test', methods=['POST'])
def test():
    result = { 'techniques': { 'names': ['SVM','RF'], 'samples': [[1,2,3],[]], 'ch_score': None, 'silhouette': None, 'results': [[4, 7, 3, 8, 9, 7], []], 'accuracy': [0.9555555555555556, 0.3], 'f1_score': [0.9552061891642257, 0.9], 'feature_importances' : [[],[]], 'confusion_matrix': [[[350,   0,   3,   2,   0,   1,   7,   1,   0,   0],
       [  0, 403,   4,   1,   0,   0,   0,   1,   2,   0],
       [  2,   0, 329,   0,   2,   0,   1,   1,   1,   0],
       [  2,   3,   7, 327,   0,   8,   1,   4,   5,   2],
       [  0,   2,   1,   0, 344,   0,   2,   2,   0,   1],
       [  0,   0,   2,   6,   2, 341,   2,   0,   2,   3],
       [  0,   1,   7,   0,   1,   1, 339,   0,   0,   0],
       [  0,   2,  11,   2,   2,   1,   0, 366,   2,   5],
       [  0,   1,   4,   1,   1,   6,   1,   1, 312,   2],
       [  0,   0,   7,   4,   3,   1,   0,   6,   1, 329]], [[350,   0,   3,   2,   0,   1,   7,   1,   0,   0],
       [  0, 403,   4,   1,   0,   0,   0,   1,   2,   0],
       [  2,   0, 329,   0,   2,   0,   1,   1,   1,   0],
       [  2,   3,   7, 327,   0,   8,   1,   4,   5,   2],
       [  0,   2,   1,   0, 344,   0,   2,   2,   0,   1],
       [  0,   0,   2,   6,   2, 341,   2,   0,   2,   3],
       [  0,   1,   7,   0,   1,   1, 339,   0,   0,   0],
       [  0,   2,  11,   2,   2,   1,   0, 366,   2,   5],
       [  0,   1,   4,   1,   1,   6,   1,   1, 312,   2],
       [  0,   0,   7,   4,   3,   1,   0,   6,   1, 329]]]}, 'best': 'SVM', 'analysis_type': 'supervised', 'education': ['https://scikit-learn.org/stable/modules/svm.html#classification', 'https://www.google.com'], 
       'labels': ['cat', 'dog','whale', 'snake', 'giraffe', 'hieu', 'mouse', 'bird', 'eagle', 'dolphin']}

    print(result)
    return jsonify(result)


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
