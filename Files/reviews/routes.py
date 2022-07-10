from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import retrieve_reviews_by_productID,add_reviews,retrieve_reviews_by_userID
from flask_cors import cross_origin, CORS

reviews = Blueprint('reviews', __name__, url_prefix='/reviews')
cors = CORS(reviews, resources={r"/foo": {"origins": "*"}})

@reviews.get('/<int:pro_con_id>')
# @jwt_required()
def get_reviews_by_productID(pro_con_id):
    result = retrieve_reviews_by_productID(pro_con_id)
    if result is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    response = jsonify(result)
    return response

@reviews.get('/<int:user_id>')
def get_reviews_by_userID(user_id):
    result = retrieve_reviews_by_userID(user_id)
    if result is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    response = jsonify(result)
    return response

@reviews.post('/<int:pro_con_id>')
def post_reviews(pro_con_id):
    if request.is_json:
        user_id = request.json.get('user_id')
        rating = request.json.get('rating')
        review = request.json.get('review')
        type = request.json.get('type')
        response = add_reviews(pro_con_id, user_id, rating, review, type)
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415