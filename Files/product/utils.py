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
    return output

def get_product_by_id(id):
    result=db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        return None
    product_schema=ProductSchema()
    output = product_schema.dump(result)
    return output

def add_product(name, description, price, image, discount, qty_left, category, related_products, seller_id):
    product=Product(name=name,description=description,price=price,image=image,
        discount=discount,effective_price=float(price)-(float(discount)*float(price)/100),
        qty_left=qty_left,related_products=related_products,seller_id=seller_id)
    db.session.add(product)
    db.session.commit()
    return {"message": "Done"}, 201

def update_product(id, name, description, price, image, discount, qty_left, category, related_products):
    product=db.session.query(Product).filter(Product.product_id==id).first()
    if not product:
        return None
    
    product.name=name
    product.description=description
    product.price=price
    product.image=image
    product.discount=discount
    product.effective_price=float(price)-(float(discount)*float(price)/100)
    product.qty_left=qty_left
    product.category=category
    product.related_products=related_products
    
    db.session.add(product)
    db.session.commit()

    return {"message": "Done"}, 202

def remove_product(id):
    product=db.session.query(Product).filter(Product.product_id==id).first()
    if not product:
        return None
    db.session.delete(product)
    db.session.commit()
    return {"message": "Done"}, 200