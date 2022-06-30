from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from .utils import AllOrdersByUser, AddOrder

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')

@orders_blueprint.get('/<int:user_id>')
def GetOrders(user_id):
    result = AllOrdersByUser(user_id)
    if not result:
        return {"message": "There are 0 orders"}, 204
    return jsonify(result), 200

@orders_blueprint.post('/<int:user_id>')
def addOrder(user_id):
    
    return 
