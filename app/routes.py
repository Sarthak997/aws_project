from app import app, mongo
from flask import request
import hashlib
from utils.generate_random import random_string_digits
from utils.access_token import generate_access_token, get_payload_from_access_token
import os

@app.route("/")
def start_page():
    print("here")
    return {
        "success": True
    }

@app.route("/user", methods= ['POST'])
def create_user():
    data = request.get_json()
    cursor = mongo.db.user.find_one({"email": data['email']})
    if cursor is not None:
        return {
            "success": False,
            "body": "user with the given email already exists"
        }
    password = data['password']
    mongo.db.user.insert_one({
        "email": data['email'],
        "password": password
    })
    return {
        "success": True
    }

@app.route('/user/login', methods = ['POST'])
def login_user():
    data = request.get_json()
    cursor = mongo.db.user.find_one({"email": data['email']})
    if cursor is None:
        return {
            "success": False,
            "body": "user with the given email does not exists"
        }
    saved_password = cursor['password']
    if data['password'] == saved_password:
        return {
            "success": True,
            "access_token": generate_access_token({
                'email': data['email']
            })
        }
    return {
        "success": False,
    }

@app.route('/instance', methods = ['POST'])
def set_user_instance():
    instances = request.get_json()['instances']
    email = get_payload_from_access_token(request.headers['token'])['email']
    mongo.db.user.update({
        "email": email
    }, {
        "$set": {
            "instances": instances
        }
    })
    return {
        "success": True
    }

@app.route('/instance', methods = ['GET'])
def get_instance_data():
    email = get_payload_from_access_token(request.headers['token'])['email']
    cursor = mongo.db.user.find_one({"email": email})
    return {
        'email': cursor['email'],
        'success': True,
        'instances': cursor['instances']
    }

