from email.policy import HTTP
from flask import Blueprint, jsonify, request
from sqlalchemy import false, true
from .utils import change_password, login_seller, register_seller, retrieve_all_sellers, retrieve_seller_byID, remove_seller, update_seller,retrieve_products_by_seller, retrieve_consultations_by_seller

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
        result = register_seller(first_name, last_name, email, password, phone, shop_name, shop_url)
        return result
    return {"message": "Request must be JSON"}, 415
    
@seller.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    result = login_seller(email, password)

    if result is true:
        return result, 200

    return result

@seller.patch('/change_password/<int:user_id>')
def patch_user_password(user_id):
    if request.is_json:
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        result = change_password(user_id, old_password, new_password)
        return result
    return {"message": "Request must be JSON"}, 415

@seller.patch('/update_details/<int:user_id>')
def patch_user_details(user_id):
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        shop_name = request.json.get('shop_name')
        shop_url = request.json.get('shop_url')
        res = update_seller(user_id, first_name, last_name, email, password, phone, shop_name, shop_url)
        if res is None:
            return {"message": "User not found"}, 204
        return res
    return {"message": "Request must be JSON"}, 415

@seller.get('/')
def get_users():
    result = retrieve_all_sellers()
    if result is None:
        return jsonify({'message': 'No users found'}), 204
    return result

@seller.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_seller_byID(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 204
    return result

@seller.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_seller(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 204
    return result

@seller.get("/products/<int:user_id>")
def get_products(user_id):
    result = retrieve_products_by_seller(user_id)
    if result is None:
        return jsonify({'message': 'No products found'}), 204
    return result

@seller.get("/consultations/<int:user_id>")
def get_consultations(user_id):
    result = retrieve_consultations_by_seller(user_id)
    if result is None:
        return jsonify({'message': 'No consultations found'}), 204
    return result