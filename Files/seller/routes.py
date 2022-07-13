from flask import Blueprint, jsonify, request
from .utils import change_password, retrieve_all_sellers, retrieve_seller_byID, remove_seller, update_seller,retrieve_products_by_seller, retrieve_consultations_by_seller
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_cors import cross_origin,CORS

seller = Blueprint('seller', __name__, url_prefix='/seller')
cors = CORS(seller, resources={r"/foo": {"origins": "*"}})

@seller.patch('/change_password/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def patch_user_password():
    if request.is_json:
        jwt_seller_id = get_jwt_identity()
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        response = change_password(jwt_seller_id, old_password, new_password)
        return response, response.status_code
    response=jsonify({"message": "Request must be JSON"})
    return response, 415

@seller.patch('/update_details/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def patch_user_details():
    if request.is_json:
        jwt_seller_id = get_jwt_identity()
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        shop_name = request.json.get('shop_name')
        shop_url = request.json.get('shop_url')
        res = update_seller(jwt_seller_id, first_name, last_name, email, password, phone, shop_name, shop_url)
        if res is None:
            response = jsonify({"message": "No user found with this ID"})
    
            return response, 204
        response = res

        return response, response.status_code
    response=jsonify({"message": "Request must be JSON"})
    return response, 415

@seller.get('/')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_users():
    result = retrieve_all_sellers()
    if result is None:
        response = jsonify({"message": "No users found"})

        return response, 204
    response = result
    return response

@seller.get('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_user_byID():
    user_id=get_jwt_identity()
    result = retrieve_seller_byID(user_id)
    if result is None:
        response = jsonify({"message": "No user found with this ID"})

        return response, 204
    response=result
    return response

@seller.delete("/")
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def delete_user():
    user_id=get_jwt_identity()
    result = remove_seller(user_id)
    if result is None:
        response = jsonify({"message": "No user found with this ID"})

        return response, 204
    response=result
    return response

@seller.get("/products/")
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_products():
    user_id=get_jwt_identity()
    result = retrieve_products_by_seller(user_id)
    if result is None:
        response = jsonify({"message": "No products found"})

        return response, 204
    response=jsonify({"result": result})
    return response

@seller.get("/consultations/")
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_consultations():
    user_id=get_jwt_identity()
    result = retrieve_consultations_by_seller(user_id)
    if result is None:
        response = jsonify({"message": "No consultations found"})

        return response, 204
    response=jsonify({"result": result})
    return response