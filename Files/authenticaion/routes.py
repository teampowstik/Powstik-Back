from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import login_user, register_user
from flask_cors import cross_origin,CORS
from pydantic import ValidationError

authentication = Blueprint('authentication', __name__)
cors = CORS(authentication, resources={r"/foo": {"origins": "*"}})

@authentication.post('/register')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def register():
    try:
        if request.is_json:
            res=request.get_json()
            result = register_user(**res)
            response=result
            return response, response.status_code
        response = jsonify({"message": "Request must be JSON"})
        return response, 415
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400
    
@authentication.post('/login')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        response = login_user(email, password)
        if response is true:
            return response,response.status_code
        return response, response.status_code
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400