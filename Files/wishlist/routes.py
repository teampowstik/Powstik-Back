from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import AddWishlist, GetWishlist, delete_item, move_to_cart
from flask_cors import CORS, cross_origin
from pydantic import ValidationError

wishlist_blueprint = Blueprint('wishlist', __name__, url_prefix='/wishlist')
cors = CORS(wishlist_blueprint, resources={r"/foo": {"origins": "*"}})

@wishlist_blueprint.get('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetWishlistItems():
    user_id = get_jwt_identity()
    result = GetWishlist(user_id)
    if not result:
        response= {"message": "There are 0 items in your wishlist"}
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response), 204
    response=jsonify(result)
    return response, 200

@wishlist_blueprint.post('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def AddToWishlist():
    try:
        if request.is_json:
            user_id = get_jwt_identity()
            res = request.get_json()
            res['user_id'] = user_id
            result = AddWishlist(**res)
            response = jsonify(result)

            return response, 200
        response=jsonify({"message": "Please send a json request"})
        return response, 415
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400

@wishlist_blueprint.delete('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteItem():
    try:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['user_id'] = user_id
        response = delete_item(**res)
        return response, response.status_code
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400

@wishlist_blueprint.patch('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def MoveToCart():
    try:
        user_id = get_jwt_identity()
        res = request.get_json()
        res['user_id'] = user_id
        response = move_to_cart(**res)
        return response, response.status_code
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400
        