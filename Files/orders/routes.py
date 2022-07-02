import re
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
def PostOrder(user_id):
    if request.is_json:
        result = request.get_json()
        result["user_id"]= user_id
        result = AddOrder(**result)
        return jsonify({"result": result}), 200
    return 
