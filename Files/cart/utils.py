from Files import db
from flask import jsonify
from Files import cors
from ..models import Cart, CartSchema, Product, Consultation

@cors
def AddCart(user_id, item_id, type):
    if type=='product':
        item=Product.query.filter_by(product_id=item_id).first()
        qty_left=int(item.qty_left)
        if qty_left<1:
            response=jsonify({"message":"Not enough quantity"})
            response.status_code=400
            return response
        effective_price=item.effective_price
        pro_con_id='P'+str(item_id)
        cart=Cart(customer_id=user_id, pro_con_id=pro_con_id, quantity=1, item_type="cart", item_total=effective_price, price=effective_price)
    elif type=='consultation':
        item=Consultation.query.filter_by(consultation_id=item_id).first()
        effective_price=item.effective_price
        pro_con_id='C'+str(item_id)
        cart=Cart(customer_id=user_id, pro_con_id=pro_con_id, quantity=1, item_type="cart", item_total=effective_price, price=effective_price)
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response

    db.session.add(cart)
    db.session.commit()
    response=jsonify({"message":"Item added to cart"})
    response.status_code=200
    return response

def GetCart(user_id):
    cart = Cart.query.filter_by(customer_id=user_id, item_type='cart').all()
    cart_schema = CartSchema(many=True)
    result = cart_schema.dump(cart)
    total_cart_price=0
    response=[]
    for item in result:
        id=item["pro_con_id"]
        total_cart_price+=item["item_total"]
        
        if id.startswith('P'):
            id=int(id[1:])
            product=Product.query.filter_by(product_id=id).first()
            name=product.name
            image=product.image
            item["name"]=name
            item["image"]=image
    
        elif id.startswith('C'):
            id=int(id[1:])
            consultation=Consultation.query.filter_by(consultation_id=id).first()
            name=consultation.consultation
            image=consultation.image
            item["name"]=name
            item["image"]=image
        
        response.append(item)

    #add total_cart_price to cart_schema
    response={"result":response,"total_cart_price":total_cart_price}
    return response

@cors
def increase_quantity(user_id, pro_con_id, type):
    if type=='product':
        id='P'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id).first()
        #check if product has enough quantity left
        item=Product.query.filter_by(product_id=pro_con_id).first()
        qty_left=int(item.qty_left)
        if qty_left<1:
            response=jsonify({"message":"Not enough quantity"})
            response.status_code=400
            return response

        cart.quantity+=1
        cart.item_total=cart.price*cart.quantity
        db.session.commit()
        response=jsonify({"message":"Quantity increased"})
        response.status_code=200
        return response
    elif type=='consultation':
        response=jsonify({"message":"Quantity is limited to 1"})
        response.status_code=400
        return response
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response

@cors
def decrease_quantity(user_id, pro_con_id, type):
    if type=='product':
        id='P'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id).first()
        if cart.quantity==1:
            response=jsonify({"message":"Quantity cannot be decreased"})
            response.status_code=400
            return response
        cart.quantity-=1
        cart.item_total=cart.price*cart.quantity
        db.session.commit()
        response=jsonify({"message":"Quantity decreased"})
        response.status_code=200
        return response
    elif type=='consultation':
        response=jsonify({"message":"Quantity is limited to 1"})
        response.status_code=400
        return response

    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response

@cors
def delete_item(user_id, pro_con_id, type):
    if type=='product':
        id='P'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id).first()
        db.session.delete(cart)
        db.session.commit()
        response=jsonify({"message":"Item deleted"})
        response.status_code=200
        return response
    elif type=='consultation':
        id='C'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id).first()
        db.session.delete(cart)
        db.session.commit()
        response=jsonify({"message":"Item deleted"})
        response.status_code=200
        return response
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response