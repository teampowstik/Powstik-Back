from cgitb import reset
from urllib import response
from sqlalchemy import desc
from Files import db
from flask import jsonify
from ..models import Order, OrderSchema, Order_Items, Order_ItemsSchema
from ..models import Cart, CartSchema, User, Address

def AllOrdersByUser(id):
    try: 
        result=db.session.query(Order).filter(Order.user_id==id).all()
        result=OrderSchema(many=True).dump(result)
    except:
        return None
    else:
        return result
    
def AddOrder(user_id=None, address_id=None):
    if not user_id or not address_id:
        response=jsonify({"message":"Missing user_id or address_id"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 400
    if db.session.query(User).filter(User.user_id==user_id).first() is None:
        response=jsonify({"message":"User not found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 400
    if db.session.query(Address).filter(Address.address_id==address_id).first() is None:
        response=jsonify({"message":"Address not found"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 400
    try:
        items=db.session.query(Cart).filter(Cart.user_id==user_id).all()
        items=CartSchema(many=True).dump(items)
        # add to order table:
        total_amout=0
        for item in items:
            total_amout+=item["price"]*item["quantity"]
        order=Order(user_id=user_id, address_id=address_id, total_amount=total_amout)
        db.session.add(order)
        # get order id:
        order=db.session.query(Order).filter(Order.user_id==user_id).order_by(desc(Order.order_id)).first()
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
    except Exception as e:
        print(e)
        response=jsonify({"message":"Error adding order"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500
    response=jsonify({"message":"Order added"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 201


    
    