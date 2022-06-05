from flask import request, jsonify, Blueprint
from flask_restful import abort, reqparse, fields, marshal_with
from Files.models import db, Product
import json

product = Blueprint('product', __name__, url_prefix='/product')

add_product_args = reqparse.RequestParser()
add_product_args.add_argument('name', type=str, required=True, help='Product name cannot be blank!')
add_product_args.add_argument('description', type=str, required=True, help='Product description cannot be blank!')
add_product_args.add_argument('price', type=float, required=True, help='Product price cannot be blank!')
add_product_args.add_argument('image', type=str, required=True, help='Product image cannot be blank!')
add_product_args.add_argument('discount', type=float, required=True, help='Product discount cannot be blank!')
add_product_args.add_argument('qty_left', type=int, required=True, help='Product qty cannot be blank!')
add_product_args.add_argument('category', type=int, required=True, help='Product category cannot be blank!')
add_product_args.add_argument('related_products', type=str, required=True, help='Product related products cannot be blank!')

resource_fields = {
    'product_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.String,
    'effective_price': fields.String,
    'image': fields.String,
    'discount': fields.String,
    'qty_left': fields.String,
    'category': fields.String,
    'related_products': fields.String,
}

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