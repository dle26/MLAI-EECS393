import pytest
import requests
from flask import jsonify
import uuid
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from app import *

url = 'http://localhost:5000'

def test_index_page():
    r = requests.get(url+'/')
    assert r.status_code == 200

def test_hello():
    r = requests.get(url+'/')
    data = r.json()

    assert data["about"] == "hello world"

def test_login_valid():
    payload = {'username': 'sadsad', 'password': '123'}
    r = requests.post(url+"/login", json=payload)

    assert r.status_code == 200

def test_login_invalid():
    payload = {'username': 'sadsad', 'password': 'junkdcfdjhd'}
    r = requests.post(url+"/login", json=payload)

    assert r.status_code == 401

def test_register():
    payload = {'username': str(uuid.uuid4()), 'password': '1234', 'firstname': 'john', 'lastname': 'doe'}
    r = requests.post(url+"/register", json=payload)

    assert r.status_code == 200

def test_register_same_username():
    name = str(uuid.uuid4())
    payload = {'username': name, 'password': '1234', 'firstname': 'john', 'lastname': 'doe'}
    r = requests.post(url+"/register", json=payload)

    r2 = requests.post(url+"/register", json=payload)

    assert r2.status_code == 422

def test_user_info():
    payload = {'username': 'sadsad'}
    r = requests.post(url+"/userinfo", json=payload)

    assert r.status_code == 200

def test_allowed_filename():
    allowed = allowed_file("test.csv")
    assert allowed == True

def test_developer_feedback():
    payload = {'email_address': 'feedback@gmail.com', 'name': 'isaac', 'feedback': 'awesome app', 'subject': 'this is cool'}
    r = requests.post(url+"/developerfeedback", json=payload)

    assert r.status_code == 200

def test_dev_register():
    payload = {'devname': str(uuid.uuid4()), 'password': '1234', 'firstname': 'john', 'lastname': 'doe'}
    r = requests.post(url+"/dev/register", json=payload)

    assert r.status_code == 200

def test_dev_login():
    name = str(uuid.uuid4())
    payload = {'devname': name, 'password': '1234', 'firstname': 'john', 'lastname': 'doe'}
    r = requests.post(url+"/dev/register", json=payload)

    payload2 = {'devname': name, 'password': '1234'}
    r2 = requests.post(url+"/dev/login", json=payload2)
    assert r2.status_code == 200
