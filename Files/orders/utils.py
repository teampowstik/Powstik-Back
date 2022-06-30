from Files import db
from flask import jsonify
from ..models import Order, OrderSchema, Order_Items, Order_ItemsSchema

def AllOrdersByUser(id):
    try: 
        result=db.session.query(Order).filter(Order.user_id==id).all()
        result=OrderSchema(many=True).dump(result)
    except:
        return None
    else:
        return result
    
def AddOrder():
    return