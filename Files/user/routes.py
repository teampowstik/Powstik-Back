from flask import Blueprint, jsonify, request
import jwt
import json
from sqlalchemy import false, true
from .utils import change_password, login_user, register_user, retrieve_all_users, retrieve_user_byID, remove_user, update_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin,CORS

user = Blueprint('user', __name__, url_prefix='/user')
cors = CORS(user, resources={r"/foo": {"origins": "*"}})

@user.post('/register')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def register():
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        result = register_user(first_name, last_name, email, password, phone)
        response=result
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415
    
@user.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    response = login_user(email, password)

    if response is true:
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response,response.status_code
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@user.patch('/change_password/<int:user_id>')
@jwt_required()
def patch_user_password(user_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            response = jsonify({"message": "You are not authorized to change this user's password"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        response = change_password(user_id, old_password, new_password)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@user.patch('/user_details/<int:user_id>')
@jwt_required()
def patch_user_details(user_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            response = jsonify({"message": "You are not authorized to change this user's details"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        res = update_user(user_id, first_name, last_name, email, password, phone)
        if res is None:
            response = jsonify({"message": "User not found"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 204
        response = res
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@user.get('/')
def get_users():
    result = retrieve_all_users()
    if result is None:
        response = jsonify({"message": "No users found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@user.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_user_byID(user_id)
    if result is None:
        response = jsonify({"message": "User not found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@user.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_user(user_id)
    if result is None:
        response = jsonify({"message": "User not found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response