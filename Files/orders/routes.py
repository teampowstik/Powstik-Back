from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .utils import AllOrdersByUser, OrderByID, OrderItemByID, AddOrder, UpdateOrder, UpdateOrderItem, RemoveOrderItem, RemoveOrder, isNotJson

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')

@orders_blueprint.get('/<int:user_id>')
def GetOrders(user_id):
    orders = AllOrdersByUser(user_id)
    return orders

@orders_blueprint.get('/<int:user_id>/<int:order_id>')
def GetOrderByID(user_id, order_id):
    order = OrderByID(user_id, order_id)
    return order

@orders_blueprint.get('/<int:user_id>/<int:order_id>/<int:item_id>')
def GetOrderItemByID(user_id, order_id, item_id):
    order_item = OrderItemByID(user_id, order_id, item_id)
    return order_item

@orders_blueprint.post('/<int:user_id>')
def PostOrder(user_id):
    if request.is_json:
        result=request.get_json()
        result['user_id']=user_id
        response=AddOrder(**result)
        return response
    
    return isNotJson()

@orders_blueprint.patch('/<int:user_id>/<int:order_id>')
def PatchOrder(user_id, order_id):
    if request.is_json:
        result=request.get_json()
        return UpdateOrder(user_id, order_id, result["address_id"]), 201
    
    return isNotJson()

@orders_blueprint.patch('/<int:user_id>/<int:order_id>/<int:order_item_id>')
def PatchOrderItem(user_id, order_id, order_item_id):
    if request.is_json:
        result=request.get_json()
        result['order_id']=order_id
        result['order_item_id']=order_item_id
        result['user_id']=user_id
        
        return UpdateOrderItem(**result)
    
    return isNotJson()
    
@orders_blueprint.delete('/<int:user_id>/<int:order_id>/<int:order_item_id>')
def DeleteOrderItem(user_id, order_id, order_item_id):
    return RemoveOrderItem(user_id, order_id, order_item_id)
    
@orders_blueprint.delete('/<int:user_id>/<int:order_id>')
def DeleteOrder(user_id, order_id):
    return RemoveOrder(user_id, order_id)
    