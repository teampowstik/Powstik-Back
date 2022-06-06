from flask import request, jsonify, Blueprint
from flask_restful import abort, marshal_with
from Files import db
from models import Product, User
import json

product = Blueprint('product', __name__, url_prefix='/product')

from .utils import add_product_args, resource_fields

@product.get('/')
@marshal_with(resource_fields)
def get_products():
    result=Product.query.all()
    return jsonify(result)

@product.get('/<int:id>')
@marshal_with(resource_fields)
def get_product(id):
    result=db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        abort(404, message="Product {} doesn't exist".format(id))
    return jsonify(result)

# @product.post('/')
# @marshal_with(resource_fields)
# def add_product():
#     if request.is_json:
#         args=add_product_args.parse_args()
#         product_name=args['name']
#         product_description=args['description']
#         product_price=args['price']
#         product_image=args['image']
#         product_discount=args['discount']
#         product_qty=args['qty_left']
#         product_category=args['category']
#         product_related_products=args['related_products']
#         product=Product(name=product_name,description=product_description,price=product_price,
#             image=product_image,discount=product_discount,effective_price=product_price-(product_discount*product_price/100),
#             qty_left=product_qty,category=product_category,related_products=product_related_products)
#         db.session.add(product)
#         db.session.commit()
#         return product, 201

#     return {"error": "Request must be JSON"}, 415

@product.post('/')
@marshal_with(resource_fields)
def add_product():
    if request.is_json:
        product=Product(name=request.json['name'],description=request.json['description'],price=request.json['price'],
            image=request.json['image'],discount=request.json['discount'],effective_price=float(request.json['price'])-(float(request.json['discount'])*float(request.json['price'])/100),
            qty_left=request.json['qty_left'],category=request.json['category'],related_products=request.json['related_products'])
        db.session.add(product)
        db.session.commit()
        return jsonify(product), 201

    return {"error": "Request must be JSON"}, 415

@product.post("/update/<integer:id>")
@marshal_with(resource_fields)
def modify_product(id):
    #modify product details like price, etc.
    if request.is_json:
        product=db.session.query(Product).filter(Product.product_id==id).first()
        args=add_product_args.parse_args()
        
        product.name=args['name']
        product.desription=args['description']
        product.price=args['price']
        product.image=args['image']
        product.discount=args['discount']
        product.qty=args['qty_left']
        product.category=args['category']
        product.related_products=args['related_products']
        
        db.session.add(product)
        db.session.commit()
        return jsonify(product), 201
    
    return {"error": "Request must be JSON"}, 415
    
    
@product.post("/delete/<integer:id>")
@marshal_with(resource_fields)
def delete_product(id):
    #delete specified product
    product=db.session.query(Product).filter(Product.product_id==id).first()
    db.session.delete(product)
    db.session.commit()
    return jsonify(product), 201
