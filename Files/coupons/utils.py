from unittest import result
from urllib import response
from flask import jsonify
from stripe import Coupon
from Files import db
from ..models import CouponsSchema, Coupons, CartSchema, Cart
import random

def generate_coupon_code():
    while True:
        res = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
        coupon = db.session.query(Coupons).filter(Coupons.coupon_code==res).first()
        coupon_schema=CouponsSchema()
        output = coupon_schema.dump(coupon)
        if not output:
            return res

def retrieve_all_coupons():
    coupons_details = db.session.query(Coupons).all()
    if not coupons_details:
        return None
    coupons_schema=CouponsSchema(many=True)
    output = coupons_schema.dump(coupons_details)
    return {"result":output}

def retrieve_coupon_id(coupon_id):
    coupon_details = db.session.query(Coupons).filter(Coupons.coupon_id==coupon_id).first()
    if not coupon_details:
        return None
    coupons_schema=CouponsSchema()
    output = coupons_schema.dump(coupon_details)
    return {"result":output}

def add_coupon(discount, limit, minimum_cart_value):
    coupon_code = generate_coupon_code()
    used = "False"

    coupon = Coupons(discount=discount, limit=limit, minimum_cart_value=minimum_cart_value, coupon_code=coupon_code, used=used)
    db.session.add(coupon)
    db.session.commit()

    return {"message": "Coupon added"}, 201

def use_coupon(coupon_code, user_id):
    coupon = db.session.query(Coupons).filter(Coupons.coupon_code==coupon_code).first()

    cart = Cart.query.filter_by(customer_id=user_id, item_type='cart').all()
    cart_schema = CartSchema(many=True)
    result = cart_schema.dump(cart)
    total_cart_price=0

    for item in result:
        total_cart_price+=item["item_total"]

    if not coupon:
        response = jsonify({"message": "Coupon not found"})
        return response, 404

    if coupon.used=="True":	
        response = jsonify({"message": "Coupon already used"})
        return response, 404

    if total_cart_price < coupon.minimum_cart_value:
        response = jsonify({"message": "Minimum cart value not met"})
        return response, 404

    coupon.used = "True"
    coupon.cart_id = 1
    db.session.commit()

    return {result : coupon}