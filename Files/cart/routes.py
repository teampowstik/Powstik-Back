from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import AddCart, GetCart, increase_quantity, decrease_quantity, delete_item

cart_blueprint = Blueprint('cart', __name__, url_prefix='/cart')

@cart_blueprint.get('/<int:user_id>')
@jwt_required()
def GetCartItems(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 401
    result = GetCart(user_id)
    if not result:
        response= jsonify({"message": "There are 0 items in your cart"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 204
        return response
    response=jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
    

@cart_blueprint.post('/<int:user_id>')
@jwt_required()
def AddToCart(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.status_code = 401
        return response
    if request.is_json:
        res = request.get_json()
        res['user_id'] = user_id
        response = AddCart(**res)
        return response
    response=jsonify({"message": "Please send a json request"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code=415 
    return response

@cart_blueprint.patch('/increaseqty/<int:user_id>')
@jwt_required()
def IncreaseQuantity(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.status_code = 401
        return response
    res = request.get_json()
    res['user_id'] = user_id
    response = increase_quantity(**res)
    return response

@cart_blueprint.patch('/decreaseqty/<int:user_id>')
@jwt_required()
def DecreaseQuantity(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 401
    res = request.get_json()
    res['user_id'] = user_id
    response = decrease_quantity(**res)
    return response

@cart_blueprint.delete('/<int:user_id>')
@jwt_required()
def DeleteItem(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 401
    res = request.get_json()
    res['user_id'] = user_id
    response = delete_item(**res)
    return response
