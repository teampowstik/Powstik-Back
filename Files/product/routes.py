from flask import request, jsonify, Blueprint
from flask_restful import abort, marshal_with
from Files.models import db, Product
import json

product = Blueprint('product', __name__, url_prefix='/product')

from .utils import add_product_args, resource_fields

@product.route('/add', methods=['POST'])

@product.get('/')
@marshal_with(resource_fields)
def get_products():
    result=db.session.query(Product).all()
    return json.dumps(result)

@product.get('/<id>')
@marshal_with(resource_fields)
def get_product(id):
    result=db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        abort(404, message="Product {} doesn't exist".format(id))
    return jsonify(result)

@product.post('/')
@marshal_with(resource_fields)
def add_product():
    if request.is_json:
        args=add_product_args.parse_args()
        product_name=args['name']
        product_description=args['description']
        product_price=args['price']
        product_image=args['image']
        product_discount=args['discount']
        product_qty=args['qty_left']
        product_category=args['category']
        product_related_products=args['related_products']
        product=Product(name=product_name,description=product_description,price=product_price,
            image=product_image,discount=product_discount,effective_price=product_price-(product_discount*product_price/100),
            qty_left=product_qty,category=product_category,related_products=product_related_products)
        db.session.add(product)
        db.session.commit()
        return product, 201

    return {"error": "Request must be JSON"}, 415