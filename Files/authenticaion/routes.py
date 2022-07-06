from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import login_user, register_user
from flask_cors import cross_origin,CORS

authentication = Blueprint('authentication', __name__)
cors = CORS(authentication, resources={r"/foo": {"origins": "*"}})

@authentication.post('/register')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def register():
    if request.is_json:
        res=request.get_json()
        result = register_user(**res)
        response=result
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415
    
@authentication.post('/login')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    response = login_user(email, password)
    if response is true:
        return response,response.status_code
    return response, response.status_code