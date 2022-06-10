from flask import Blueprint, jsonify, request
from .utils import get_all_products, get_product_by_id, add_product, update_product, remove_product

product = Blueprint('product', __name__, url_prefix='/product')

@product.get('/')
def get_products():
    result=get_all_products()
    if result is None:
       return {"message": "There are 0 products"}, 204
    return jsonify(result), 200

@product.get('/<int:id>')
def get_product(id):
    result = get_product_by_id(id)
    if result is None:
        return {}, 204
    return jsonify(result), 200

@product.post('/')
def post_product():
    if request.is_json:
        name=request.json['name']
        description=request.json['description']
        price=request.json['price']
        image=request.json['image']
        discount=request.json['discount']
        qty_left=request.json['qty_left']
        category=request.json['category']
        related_products=request.json['related_products']
        add_product(name, description, price, image, discount, qty_left, category, related_products)
        return {"message": "Done"}, 201
    return {"message": "Request must be JSON"}, 415
        

@product.patch("/<int:id>")
def patch_product(id):
    if request.is_json:
        name=request.json['name']
        description=request.json['description']
        price=request.json['price']
        image=request.json['image']
        discount=request.json['discount']
        qty_left=request.json['qty_left']
        category=request.json['category']
        related_products=request.json['related_products']
        res=update_product(id, name, description, price, image, discount, qty_left, category, related_products)
        if res is None:
            return {}, 204
        return {"message": "Done"}, 202
    return {"message": "Request must be JSON"}, 415

@product.delete("/<int:id>")
def delete_product(id):
    res = remove_product(id)
    if res is None:
        return {}, 204
    return {"message": "Done"}, 200
