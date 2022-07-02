from flask import Blueprint, jsonify, request
import jwt
import json
from sqlalchemy import false, true
from .utils import change_password, login_user, register_user, retrieve_all_users, retrieve_user_byID, remove_user, update_user
from flask_jwt_extended import get_jwt_identity, jwt_required


user = Blueprint('user', __name__, url_prefix='/user')

@user.get('/test')
def dummy_route():
    return {"message": "Working"}, 200

@user.post('/register')
def register():
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        result = register_user(first_name, last_name, email, password, phone)
        return result
    return {"message": "Request must be JSON"}, 415
    
@user.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    result = login_user(email, password)

    if result is true:
        return result

    return result

@user.patch('/change_password/<int:user_id>')
@jwt_required()
def patch_user_password(user_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            return {"message": "You are not authorized to change this user's password"}, 401
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        result = change_password(user_id, old_password, new_password)
        return result
    return {"message": "Request must be JSON"}, 415

@user.patch('/user_details/<int:user_id>')
@jwt_required()
def patch_user_details(user_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            return {"message": "You are not authorized to change this user's details"}, 401
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        res = update_user(user_id, first_name, last_name, email, password, phone)
        if res is None:
            return {"message": "User not found"}, 204
        return res
    return {"message": "Request must be JSON"}, 415

@user.get('/')
def get_users():
    result = retrieve_all_users()
    if result is None:
        return jsonify({'message': 'No users found'}), 204
    return jsonify(result)

@user.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_user_byID(user_id)
    if result is None:
        return {'message': 'User not found'}, 204
    return jsonify(result), 200

@user.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_user(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 204
    return result