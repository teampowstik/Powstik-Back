from flask_restful import reqparse, fields

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