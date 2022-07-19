from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import get_reviews_with_user_utils, retrieve_reviews_by_productID,add_reviews,retrieve_reviews_by_userID, get_reviews_with_user_utils, get_ratings_utils
from flask_cors import cross_origin, CORS

reviews = Blueprint('reviews', __name__, url_prefix='/reviews')
cors = CORS(reviews, resources={r"/foo": {"origins": "*"}})

@reviews.get('/<string:pro_con_id>')
# @jwt_required()
def get_reviews_by_productID(pro_con_id):
    result = retrieve_reviews_by_productID(pro_con_id)
    if result is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    response = jsonify(result)
    return response

@reviews.get('/')
@jwt_required()
def get_reviews_by_userID():
    user_id = get_jwt_identity()
    result = retrieve_reviews_by_userID(user_id)
    if result is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    response = jsonify(result)
    return response

@reviews.post('/<string:pro_con_id>')
@jwt_required()
def post_reviews(pro_con_id):
    if request.is_json:
        user_id = get_jwt_identity()
        rating = request.json.get('rating')
        review = request.json.get('review')
        type = request.json.get('type')
        response = add_reviews(pro_con_id, user_id, rating, review, type)
        return response
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@reviews.get('/reviews_with_user/<string:pro_con_id>')
def get_reviews_with_user(pro_con_id):
    result = get_reviews_with_user_utils(pro_con_id)
    if result is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    response = jsonify(result)
    return response

@reviews.get('/ratings/<string:pro_con_id>')
def get_ratings(pro_con_id):
    response = get_ratings_utils(pro_con_id)
    if response is None:
        response = jsonify({"message": "No reviews found"})
        return response, 204
    return response
    