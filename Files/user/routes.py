from email.policy import HTTP
from unittest import result
from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import change_password, login_user, register_user, retrieve_all_users, retrieve_user_byID, remove_user, update_user
from flask_jwt_extended import get_jwt_identity, jwt_required

user = Blueprint('user', __name__, url_prefix='/user')

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

    return result, 404

@user.patch('/change password/<int:user_id>')
def patch_user_password(user_id):
    if request.is_json:
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        result = change_password(user_id, old_password, new_password)
        return result
    return {"message": "Request must be JSON"}, 415

@user.patch('/user details/<int:user_id>')
def patch_user_details(user_id):
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        res = update_user(user_id, first_name, last_name, email, password, phone)
        if res is None:
            return {"message": "User not found"}, 404
        return res
    return {"message": "Request must be JSON"}, 415

@user.get('/')
def get_users():
    result = retrieve_all_users()
    if result is None:
        return jsonify({'message': 'No users found'}), 404
    return jsonify(result)

@user.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_user_byID(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 404
    return jsonify(result)

@user.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_user(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 404
    return result