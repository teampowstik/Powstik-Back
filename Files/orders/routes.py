from unittest import result
from urllib import response
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import isOrderThere, isAddressThere, AllOrdersByUser, AddOrder, UpdateOrder, UpdateOrderItem

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')

@orders_blueprint.get('/<int:user_id>')
def GetOrders(user_id):
    orders = AllOrdersByUser(user_id)
    if not orders:
        response = jsonify({'message': 'No orders found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    return orders, 200

@orders_blueprint.post('/<int:user_id>')
def PostOrder(user_id):
    if request.is_json:
        result=request.get_json()
        result['user_id']=user_id
        
        if not isAddressThere(result["address_id"]):
            response = jsonify({'message': 'Address not found'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        
        response=AddOrder(**result)
        return response, 200
    # CORS Functionality implemented in the function due to complexity of the code
    return 404

@orders_blueprint.patch('/<int:user_id>/<int:order_id>')
def PatchOrder(user_id, order_id):
    if not isOrderThere(order_id, user_id):
        response = jsonify({'message': 'Order not found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 404
    
    if request.is_json:
        result=request.get_json()
        if not isAddressThere(result["address_id"]):
            response = jsonify({'message': 'Address not found'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 404
        
        return UpdateOrder(user_id, order_id, result["address_id"]), 201
    
    response = jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 500

@orders_blueprint.patch('/<int:user_id>/<int:order_id>/<int:order_item_id>')
def PatchOrderItem(user_id, order_id, order_item_id):
    if not isOrderThere(order_id, user_id):
        response = jsonify({'message': 'Order not found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 404
    
    if request.is_json:
        result=request.get_json()
        result['order_id']=order_id
        result['order_item_id']=order_item_id
        result['user_id']=user_id
        
        return UpdateOrderItem(**result), 201
    
    response = jsonify({"message": "Request must be JSON"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 500
    