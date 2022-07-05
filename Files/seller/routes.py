from email.policy import HTTP
from urllib import response
from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import change_password, login_seller, register_seller, retrieve_all_sellers, retrieve_seller_byID, remove_seller, update_seller,retrieve_products_by_seller, retrieve_consultations_by_seller
from flask_jwt_extended import get_jwt_identity, jwt_required

seller = Blueprint('seller', __name__, url_prefix='/seller')


@seller.post('/register')
def register():
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        shop_name = request.json.get('shop_name')
        shop_url = request.json.get('shop_url')
        response = register_seller(first_name, last_name, email, password, phone, shop_name, shop_url)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415
    
@seller.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    result = login_seller(email, password)

    if result is true:
        response=result
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code

    response = result
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@seller.patch('/change_password/<int:seller_id>')
@jwt_required()
def patch_user_password(seller_id):
    if request.is_json:
        jwt_seller_id = get_jwt_identity()
        if jwt_seller_id != seller_id:
            response = jsonify({"message": "You are not authorized to change this user's password"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        response = change_password(seller_id, old_password, new_password)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response=jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@seller.patch('/update_details/<int:seller_id>')
@jwt_required()
def patch_user_details(seller_id):
    if request.is_json:
        jwt_seller_id = get_jwt_identity()
        if jwt_seller_id != seller_id:
            response = jsonify({"message": "You are not authorized to change this user's details"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        shop_name = request.json.get('shop_name')
        shop_url = request.json.get('shop_url')
        res = update_seller(seller_id, first_name, last_name, email, password, phone, shop_name, shop_url)
        if res is None:
            response = jsonify({"message": "No user found with this ID"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 204
        response = res
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response=jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@seller.get('/')
def get_users():
    result = retrieve_all_sellers()
    if result is None:
        response = jsonify({"message": "No users found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = result
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@seller.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_seller_byID(user_id)
    if result is None:
        response = jsonify({"message": "No user found with this ID"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response=result
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@seller.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_seller(user_id)
    if result is None:
        response = jsonify({"message": "No user found with this ID"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response=result
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@seller.get("/products/<int:user_id>")
def get_products(user_id):
    result = retrieve_products_by_seller(user_id)
    if result is None:
        response = jsonify({"message": "No products found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response=jsonify({"result": result})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@seller.get("/consultations/<int:user_id>")
def get_consultations(user_id):
    result = retrieve_consultations_by_seller(user_id)
    if result is None:
        response = jsonify({"message": "No consultations found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response=jsonify({"result": result})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response