from flask import Blueprint, jsonify, request
from .utils import get_all_products, get_product_by_id, products_by_category, add_product, update_product, remove_product
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS

product = Blueprint('product', __name__, url_prefix='/product')
cors = CORS(product, resources={r"/foo": {"origins": "*"}})

@product.get('/')
def get_products():
    result=get_all_products()
    if result is None:
        response = jsonify({'message': 'No products found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response =  jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@product.get('/<int:id>')
def get_product(id):
    result = get_product_by_id(id)
    if result is None:
        response={}
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    return (result), 200

@product.get('/bycategory/<string:category_name>')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_product_by_category_name(category_name):
    result = products_by_category(category_name)
    if result is None:
        response={}
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response =  jsonify({"result": result})
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@product.post('/')
@jwt_required()
def post_product():
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        res['seller_id'] = seller_id
        response = add_product(**res)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415
        

@product.patch("/<int:product_id>")
@jwt_required()
def patch_product(product_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        res = request.get_json()
        res["product_id"] = product_id
        res['seller_id'] = seller_id
        response = update_product(**res)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@product.delete("/<int:product_id>")
@jwt_required()
def delete_product(product_id):
    seller_id = get_jwt_identity()
    res = remove_product(product_id, seller_id=seller_id)
    if res is None:
        response = jsonify({'message': 'No product found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response=res
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, response.status_code