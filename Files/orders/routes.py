from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS
from .utils import AllOrdersByUser, OrderByID, OrderItemByID, AddOrder, UpdateOrder, UpdateOrderItem, RemoveOrderItem, RemoveOrder, isNotJson

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')
cors = CORS(orders_blueprint, resources={r"/foo": {"origins": "*"}})

@orders_blueprint.get('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrders():
    user_id = get_jwt_identity()
    orders = AllOrdersByUser(user_id)
    return orders

@orders_blueprint.get('/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrderByID(order_id):
    user_id = get_jwt_identity()
    order = OrderByID(user_id, order_id)
    return order

@orders_blueprint.get('/<int:order_id>/<int:item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetOrderItemByID(order_id, item_id):
    user_id = get_jwt_identity()
    order_item = OrderItemByID(user_id, order_id, item_id)
    return order_item

@orders_blueprint.post('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PostOrder():
    user_id = get_jwt_identity()
    if request.is_json:
        result=request.get_json()
        result['user_id']=user_id
        response=AddOrder(**result)
        return response
    return isNotJson()

@orders_blueprint.patch('/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchOrder(order_id):
    user_id = get_jwt_identity()
    if request.is_json:
        result=request.get_json()
        return UpdateOrder(user_id, order_id, result["address_id"]), 201
    return isNotJson()

@orders_blueprint.patch('/<int:order_id>/<int:order_item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchOrderItem(order_id, order_item_id):
    user_id = get_jwt_identity()
    if request.is_json:
        result=request.get_json()
        result['order_id']=order_id
        result['order_item_id']=order_item_id
        result['user_id']=user_id
        
        return UpdateOrderItem(**result)
    return isNotJson()
    
@orders_blueprint.delete('/<int:order_id>/<int:order_item_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteOrderItem(order_id, order_item_id):
    user_id = get_jwt_identity()
    return RemoveOrderItem(user_id, order_id, order_item_id)
    
@orders_blueprint.delete('/<int:order_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteOrder(order_id):
    user_id = get_jwt_identity()
    return RemoveOrder(user_id, order_id)
    