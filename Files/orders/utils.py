from sqlalchemy import desc
from Files import db
from flask import jsonify
from ..models import Order, OrderSchema, Order_Items, Order_ItemsSchema
from ..models import Cart, CartSchema

def AllOrdersByUser(id):
    try: 
        result=db.session.query(Order).filter(Order.user_id==id).all()
        result=OrderSchema(many=True).dump(result)
    except:
        return None
    else:
        return result
    
def AddOrder(user_id, address_id, amount, order_items):
        #cost_check
    if amount == 0:
        return {"message": "The cost of the order is 0"}, 400
        #address_check
    if address_id == None:
        return {"message": "The address is not specified"}, 400
    try:
        total=0
        for order_item in order_items:
            temp_price=order_item["price"]*order_item["quantity"]    
            total=total+temp_price
        if total != amount:
            return {"message": "The total cost of the order is not equal to the amount"}, 400
        
        order = Order(customer_id=user_id, address_id=address_id, amount=amount)
        order = db.session.query(Order).filter(
            Order.customer_id==user_id).filter(
                Order.amount==amount).order_by(desc).first()
            
        db.session.add(order)
        
        for order_item in order_items:
            order_item_ = Order_Items(order_id=order.order_id, pro_con_id=order_item["pro_con_id"], quantity=order_item["quantity"], price=order_item["price"])
            db.session.add(order_item_)
        db.session.query(Cart).filter(Cart.customer_id==user_id).delete()
        db.session.commit()
        return {"message": "Order added successfully"}, 201
    except:
        return {"message": "Something went wrong"}, 400