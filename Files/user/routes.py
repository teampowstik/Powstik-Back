from flask import Blueprint, jsonify, request
import jwt
import json
from sqlalchemy import false, true
from .utils import change_password, retrieve_all_users, retrieve_user_byID, remove_user, update_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin,CORS

user = Blueprint('user', __name__, url_prefix='/user')
cors = CORS(user, resources={r"/foo": {"origins": "*"}})

@user.patch('/change_password/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def patch_user_password():
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        response = change_password(jwt_user_id, old_password, new_password)

        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@user.patch('/user_details/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def patch_user_details():
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        res = update_user(jwt_user_id, first_name, last_name, email, password, phone)
        if res is None:
            response = jsonify({"message": "User not found"})
    
            return response, 204
        response = res

        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@user.get('/')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_users():
    result = retrieve_all_users()
    if result is None:
        response = jsonify({"message": "No users found"})

        return response, 204
    response = jsonify(result)
    return response

@user.get('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_user_byID():
    user_id=get_jwt_identity()
    result = retrieve_user_byID(user_id)
    if result is None:
        response = jsonify({"message": "User not found"})

        return response, 204
    response = jsonify(result)
    return response, 200

@user.delete("/")
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def delete_user():
    user_id=get_jwt_identity()
    result = remove_user(user_id)
    if result is None:
        response = jsonify({"message": "User not found"})

        return response, 204
    response = jsonify(result)
    return response