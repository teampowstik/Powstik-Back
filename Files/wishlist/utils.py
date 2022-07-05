from Files import db
from flask import jsonify
from ..models import Cart, CartSchema, Product, Consultation

def AddWishlist(user_id, item_id, type):
    if type=='product':
        item=Product.query.filter_by(product_id=item_id).first()
        effective_price=item.effective_price
        pro_con_id='P'+str(item_id)
        cart=Cart(customer_id=user_id, pro_con_id=pro_con_id, quantity=1, item_type="wishlist", item_total=effective_price, price=effective_price)
    elif type=='consultation':
        item=Consultation.query.filter_by(consultation_id=item_id).first()
        effective_price=item.effective_price
        pro_con_id='C'+str(item_id)
        cart=Cart(customer_id=user_id, pro_con_id=pro_con_id, quantity=1, item_type="wishlist", item_total=effective_price, price=effective_price)
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response
        
    db.session.add(cart)
    db.session.commit()
    return {"message":"Item added to wishlist"}

def GetWishlist(user_id):
    cart = Cart.query.filter_by(customer_id=user_id, item_type='wishlist').all()
    cart_schema = CartSchema(many=True)
    result = cart_schema.dump(cart)
    response=[]
    for item in result:
        id=item["pro_con_id"]
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

    response={"result":response}
    return response

def delete_item(user_id, pro_con_id, type):
    if type=='product':
        id='P'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id, item_type='wishlist').first()
        db.session.delete(cart)
        db.session.commit()
        response=jsonify({"message":"Item deleted"})
        response.status_code=200
        return response
    elif type=='consultation':
        id='C'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id, item_type='wishlist').first()
        db.session.delete(cart)
        db.session.commit()
        response=jsonify({"message":"Item deleted"})
        response.status_code=200
        return response
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response

def move_to_cart(user_id, pro_con_id, type):
    if type=='product':
        id='P'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id, item_type='wishlist').first()
        cart.item_type='cart'
        db.session.commit()
        response=jsonify({"message":"Item moved to cart"})
        response.status_code=200
        return response
    elif type=='consultation':
        id='C'+str(pro_con_id)
        cart=Cart.query.filter_by(customer_id=user_id, pro_con_id=id, item_type='wishlist').first()
        cart.item_type='cart'
        db.session.commit()
        response=jsonify({"message":"Item moved to cart"})
        response.status_code=200
        return response
    else:
        response=jsonify({"message":"Wrong type"})
        response.status_code=400
        return response