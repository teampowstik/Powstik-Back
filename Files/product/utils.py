from flask_restful import reqparse
from flask import request, jsonify
from Files import db
from ..models import Product, ProductSchema


add_product_args = reqparse.RequestParser()
add_product_args.add_argument('name', type=str, required=True, help='Product name cannot be blank!')
add_product_args.add_argument('description', type=str, required=True, help='Product description cannot be blank!')
add_product_args.add_argument('price', type=float, required=True, help='Product price cannot be blank!')
add_product_args.add_argument('image', type=str, required=True, help='Product image cannot be blank!')
add_product_args.add_argument('discount', type=float, required=True, help='Product discount cannot be blank!')
add_product_args.add_argument('qty_left', type=int, required=True, help='Product qty cannot be blank!')
add_product_args.add_argument('category', type=int, required=True, help='Product category cannot be blank!')
add_product_args.add_argument('related_products', type=str, required=True, help='Product related products cannot be blank!')


def get_all_products():
    result=Product.query.all()
    product_schema=ProductSchema(many=True)
    output = product_schema.dump(result)
    return jsonify(output)

def get_product_by_id(id):
    result=db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        return {"message": "No product found"}, 404
    product_schema=ProductSchema()
    output = product_schema.dump(result)
    return jsonify(output)

def add_product():
    if request.is_json:
        product=Product(name=request.json['name'],description=request.json['description'],price=request.json['price'],
            image=request.json['image'],discount=request.json['discount'],effective_price=float(request.json['price'])-(float(request.json['discount'])*float(request.json['price'])/100),
            qty_left=request.json['qty_left'],category=request.json['category'],related_products=request.json['related_products'])
        db.session.add(product)
        db.session.commit()
        return {"message": "Done"}, 201

    return {"message": "Request must be JSON"}, 415

def update_product(id):
    if request.is_json:
        product=db.session.query(Product).filter(Product.product_id==id).first()
        if not product:
            return {"message": "No product found"}, 404
        
        product.name=request.json['name']
        product.description=request.json['description']
        product.price=request.json['price']
        product.image=request.json['image']
        product.discount=request.json['discount']
        product.effective_price=float(request.json['price'])-(float(request.json['discount'])*float(request.json['price'])/100)
        product.qty_left=request.json['qty_left']
        product.category=request.json['category']
        product.related_products=request.json['related_products']
        
        db.session.add(product)
        db.session.commit()

        return {"message": "Done"}, 201
    
    return {"error": "Request must be JSON"}, 415

def remove_product(id):
    product=db.session.query(Product).filter(Product.product_id==id).first()
    if not product:
        return {"message": "No product found"}, 404
    db.session.delete(product)
    db.session.commit()
    return {"message": "Done"}, 200