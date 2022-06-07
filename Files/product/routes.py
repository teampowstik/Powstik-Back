from flask import Blueprint
from .utils import get_all_products, get_product_by_id, add_product, update_product, remove_product

product = Blueprint('product', __name__, url_prefix='/product')

@product.get('/')
def get_products():
    return get_all_products()

@product.get('/<int:id>')
def get_product(id):
    return get_product_by_id(id)

@product.post('/')
def post_product():
    return add_product()

@product.patch("/<int:id>")
def patch_product(id):
    return update_product(id)
    
@product.delete("/<int:id>")
def delete_product(id):
    return remove_product(id)
