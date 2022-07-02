from cgitb import reset
import re
from urllib import response
from sqlalchemy import desc
from Files import db, cors
from flask import jsonify
from ..models import Order, OrderSchema, Order_Items, Order_ItemsSchema
from ..models import Cart, CartSchema, User, Address

#Boolean Functions
def isOrderThere(order_id,user_id):
    return db.session.query(Order).filter(Order.order_id==order_id).filter(Order.customer_id==user_id).first() is not None

def isAddressThere(address_id):
    return db.session.query(Address).filter(Address.address_id==address_id).first() is not None

#Response Functions
@cors
def AllOrdersByUser(id):
    orders=db.session.query(Order).filter(Order.customer_id==id).all()
    orders=OrderSchema(many=True).dump(orders)
    # add order items to each order
    for order in orders:
        order_items=db.session.query(Order_Items).filter(Order_Items.order_id==order["order_id"]).all()
        order_items=Order_ItemsSchema(many=True).dump(order_items)
        order["order_items"]=order_items
    response=jsonify(orders)
    return response

@cors
def AddOrder(user_id=None, address_id=None):
    items=db.session.query(Cart).filter(Cart.customer_id==user_id).all()
    items=CartSchema(many=True).dump(items)
    # add to order table:
    total_amout=0
    for item in items:
        total_amout+=item["price"]*item["quantity"]
    order=Order(customer_id=user_id, address_id=address_id, amount=total_amout)
    db.session.add(order)
    # get order id:
    order=db.session.query(Order).filter(Order.customer_id==user_id).order_by(desc(Order.order_id)).first()
    order=OrderSchema(many=False).dump(order)
    order_id=order["order_id"]   
    # add order items:
    for item in items:
        order_item=Order_Items(
            order_id=order_id, 
            pro_con_id=item["pro_con_id"], 
            quantity=item["quantity"], 
            price=item["price"],
            status="Processing"
            )
        db.session.add(order_item)
    db.session.commit()
    response=jsonify({"message":"Order added"})
    return response

@cors
def UpdateOrder(user_id=None, order_id=None, address_id=None):
    if not user_id or not order_id or not address_id:
        response=jsonify({"message":"Missing user_id, order_id or address_id"})
    order=db.session.query(Order).filter(Order.order_id==order_id).first()
    order.address_id=address_id
    db.session.commit()
    response=jsonify({"message":"Address updated"})
    return response

# for sellers to change status of the order
@cors
def UpdateOrderItem(user_id, order_id, order_item_id, status, tracking_id, tracking_number):
    order_item=db.session.query(Order_Items).filter(Order_Items.order_item_id==order_item_id).filter(Order_Items.order_id==order_id).first()
    order_item.status=status
    # Processing
    # In Transit
    # Shipped
    # Delivered
    order_item.tracking_id=tracking_id
    order_item.tracking_number=tracking_number
    db.session.commit()
    response=jsonify({"message":"Order item updated"})
    return response
    