from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import AddCart, GetCart, increase_quantity, decrease_quantity, delete_item
from flask_cors import cross_origin, CORS

cart_blueprint = Blueprint('cart', __name__, url_prefix='/cart')
cors = CORS(cart_blueprint, resources={r"/foo": {"origins": "*"}})

@cart_blueprint.get('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetCartItems():
    user_id = get_jwt_identity()
    result = GetCart(user_id)
    if not result:
        response= {"message": "There are 0 items in your cart"}
        return jsonify(response), 204
    response=jsonify(result)
    return response, 200
    

@cart_blueprint.post('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def AddToCart():
    if request.is_json:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['user_id'] = user_id
        response = AddCart(**res)

        return response, response.status_code
    response=jsonify({"message": "Please send a json request"})
    return response, 415

@cart_blueprint.patch('/increaseqty/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def IncreaseQuantity():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = increase_quantity(**res)
    return response, response.status_code

@cart_blueprint.patch('/decreaseqty/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DecreaseQuantity():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = decrease_quantity(**res)
    return response, response.status_code

@cart_blueprint.delete('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteItem():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = delete_item(**res)
    return response, response.status_code
