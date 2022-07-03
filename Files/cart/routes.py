from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import AddCart, GetCart, increase_quantity, decrease_quantity, delete_item

cart_blueprint = Blueprint('cart', __name__, url_prefix='/cart')

@cart_blueprint.get('/')
@jwt_required()
def GetCartItems():
    user_id = get_jwt_identity()
    result = GetCart(user_id)
    if not result:
        response= {"message": "There are 0 items in your cart"}
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response), 204
    response=jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200
    

@cart_blueprint.post('/')
@jwt_required()
def AddToCart():
    if request.is_json:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['user_id'] = user_id
        response = AddCart(**res)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response=jsonify({"message": "Please send a json request"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@cart_blueprint.patch('/increaseqty/')
@jwt_required()
def IncreaseQuantity():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = increase_quantity(**res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@cart_blueprint.patch('/decreaseqty/')
@jwt_required()
def DecreaseQuantity():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = decrease_quantity(**res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@cart_blueprint.delete('/')
@jwt_required()
def DeleteItem():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = delete_item(**res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@cart_blueprint.post('/')
@jwt_required()
def AddToWishlist():
    if request.is_json:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['customer_id'] = user_id
        result = AddWishlist(**res)
        return jsonify({"result": result}), 200
    return {"message": "Request must be JSON"}, 415
    
