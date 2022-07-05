from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import add_address_util, retrieve_all_addresses, retrieve_address_byUserID, remove_address, update_address_util
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin,CORS


address = Blueprint('address', __name__, url_prefix='/address')
cors = CORS(address, resources={r"/foo": {"origins": "*"}})

@address.post('/add/<int:user_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def add_address(user_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            return {"message": "You are not authorized to add an address"}, 401
        line1 = request.json.get('line1')
        line2 = request.json.get('line2')
        city = request.json.get('city')
        state = request.json.get('state')
        country = request.json.get('country')
        zipcode = request.json.get('zipcode')
        password = request.json.get('password')
        result = add_address_util(user_id, line1, line2, city, state, country, zipcode, password)
        return result
    return {"message": "Request must be JSON"}, 415

@address.get('/')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_addresses():
    result = retrieve_all_addresses()
    if result is None:
        return {"message": "No addresses found"}, 404
    return jsonify(result)

@address.get('/<int:user_id>')
def retrieve_address_byID(user_id):
    result = retrieve_address_byUserID(user_id)
    if result is None:
        return {"message": "No addresses found"}, 404
    return jsonify(result)

@address.patch('/<int:user_id> <int:address_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def update_address(user_id, address_id):
    if request.is_json:
        jwt_user_id = get_jwt_identity()
        if jwt_user_id != user_id:
            return {"message": "You are not authorized to update this address"}, 401
        line1 = request.json.get('line1')
        line2 = request.json.get('line2')
        city = request.json.get('city')
        state = request.json.get('state')
        country = request.json.get('country')
        zipcode = request.json.get('zipcode')
        result = update_address_util(user_id, address_id, line1, line2, city, state, country, zipcode)
        return result
    return {"message": "Request must be JSON"}, 415

@address.delete('/<int:user_id> <int:address_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def delete_address(user_id, address_id):
    jwt_user_id = get_jwt_identity()
    if jwt_user_id != user_id:
        return {"message": "You are not authorized to delete this address"}, 401
    result = remove_address(user_id, address_id)
    return result