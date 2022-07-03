from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import AddWishlist, GetWishlist, delete_item, move_to_cart

wishlist_blueprint = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@wishlist_blueprint.get('/')
@jwt_required()
def GetWishlistItems():
    user_id = get_jwt_identity()
    result = GetWishlist(user_id)
    if not result:
        response= {"message": "There are 0 items in your wishlist"}
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response), 204
    response=jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@wishlist_blueprint.post('/')
@jwt_required()
def AddToWishlist():
    if request.is_json:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['user_id'] = user_id
        result = AddWishlist(**res)
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200
    response=jsonify({"message": "Please send a json request"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 415

@wishlist_blueprint.delete('/')
@jwt_required()
def DeleteItem():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = delete_item(**res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code

@wishlist_blueprint.patch('/')
@jwt_required()
def MoveToCart():
    user_id = get_jwt_identity()
    res = request.get_json()
    res['user_id'] = user_id
    response = move_to_cart(**res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code