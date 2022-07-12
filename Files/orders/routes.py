from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS
from .utils import AllOrdersByUser, OrderByID, OrderItemByID, AddOrder, UpdateOrder, UpdateOrderItem, RemoveOrderItem, RemoveOrder, isNotJson

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')
cors = CORS(orders_blueprint, resources={r"/foo": {"origins": "*"}})

@orders_blueprint.get('/<int:user_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrders(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    orders = AllOrdersByUser(user_id)
    return orders

@orders_blueprint.get('/<int:user_id>/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrderByID(user_id, order_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    order = OrderByID(user_id, order_id)
    return order

@orders_blueprint.get('/<int:user_id>/<int:order_id>/<int:item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrderItemByID(user_id, order_id, item_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    order_item = OrderItemByID(user_id, order_id, item_id)
    return order_item

@orders_blueprint.post('/<int:user_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PostOrder(user_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    if request.is_json:
        result=request.get_json()
        result['user_id']=user_id
        response=AddOrder(**result)
        return response
    
    return isNotJson()

@orders_blueprint.patch('/<int:user_id>/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchOrder(user_id, order_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    if request.is_json:
        result=request.get_json()
        return UpdateOrder(user_id, order_id, result["address_id"]), 201
    
    return isNotJson()

@orders_blueprint.patch('/<int:user_id>/<int:order_id>/<int:order_item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchOrderItem(user_id, order_id, order_item_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    if request.is_json:
        result=request.get_json()
        result['order_id']=order_id
        result['order_item_id']=order_item_id
        result['user_id']=user_id
        
        return UpdateOrderItem(**result)
    return isNotJson()
    
@orders_blueprint.delete('/<int:user_id>/<int:order_id>/<int:order_item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteOrderItem(user_id, order_id, order_item_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    return RemoveOrderItem(user_id, order_id, order_item_id)
    
@orders_blueprint.delete('/<int:user_id>/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteOrder(user_id, order_id):
    if user_id != get_jwt_identity():
        response = jsonify({"message": "You are not authorized to get this user's orders"})
        return response, 401
    return RemoveOrder(user_id, order_id)
    