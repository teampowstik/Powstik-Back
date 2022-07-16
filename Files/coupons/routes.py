from flask import Blueprint, request, jsonify
from torch import minimum
from .utils import retrieve_all_coupons, retrieve_coupon_id, add_coupon, use_coupon
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_cors import cross_origin, CORS

coupons = Blueprint('coupons', __name__, url_prefix='/coupons')
cors = CORS(coupons, resources={r"/foo": {"origins": "*"}})

@coupons.get('/')
def get_coupons():
    result = retrieve_all_coupons()
    if result is None:
        response = jsonify({"message": "No coupons found"})
        return response, 204
    response = jsonify(result)
    return response

@coupons.get('/<int:coupon_id>')
def get_coupon_id(coupon_id):
    result = retrieve_coupon_id(coupon_id)
    if result is None:
        response = jsonify({"message": "No coupons found"})
        return response, 204
    response = jsonify(result)
    return response

@coupons.post('/')
def post_coupons():
    if request.is_json:
        discount = request.json.get('discount')
        limit = request.json.get('limit')
        minimum_cart_value = request.json.get('minimum_cart_value')
        response = add_coupon(discount, limit, minimum_cart_value)
        return response
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@coupons.post('/<string:coupon_code>')
@jwt_required()
def use_coupon_by_id(coupon_code):
    user_id = get_jwt_identity()
    response = use_coupon(coupon_code, user_id)
    return response

