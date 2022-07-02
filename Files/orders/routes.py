import re
from unittest import result
from urllib import response
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from .utils import AllOrdersByUser, AddOrder

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')

@orders_blueprint.get('/<int:user_id>')
def GetOrders(user_id):
    result = AllOrdersByUser(user_id)
    if not result:
        response = jsonify({'message': 'No orders found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return {"message": "There are 0 orders"}, 204
    response=jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@orders_blueprint.post('/<int:user_id>')
def PostOrder(user_id):
    if request.is_json:
        result=request.get_json()
        result['user_id']=user_id
        return AddOrder(**result)
    return 404
