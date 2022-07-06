from urllib import response
from flask import request, jsonify
from Files import db
from ..models import User, Seller, UserSchema, SellerSchema, Product, ProductSchema, Consultation, ConsultationSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from sqlalchemy import or_

def retrieve_all_sellers():
    sellers=db.session.query(Seller).all()
    seller_schema=SellerSchema(many=True)
    seller_output = seller_schema.dump(sellers)
    for seller in seller_output:
        user=db.session.query(User).filter(User.user_id==seller["seller_id"]).first()
        user_schema=UserSchema()
        output = user_schema.dump(user)
        seller.update(output)
    return jsonify({"result":seller_output})


def retrieve_seller_byID(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    seller_details=db.session.query(Seller).filter(Seller.seller_id==user_id).first()
    if not user_details or not seller_details:
        return {"message": "User not found"}, 404
    user_schema=UserSchema()
    output_user = user_schema.dump(user_details)
    seller_schema=SellerSchema()
    output_seller = seller_schema.dump(seller_details)
    return jsonify({"user": output_user, "seller": output_seller})


def remove_seller(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    seller_details=db.session.query(Seller).filter(Seller.seller_id==user_id).first()
    if not user_details or not seller_details:
        return None
    db.session.delete(user_details)
    db.session.delete(seller_details)
    db.session.commit()
    return {"message": "User Successfully deleted"}, 201


def update_seller(seller_id, first_name, last_name, email, password, phone, shop_name, shop_url):
    user=db.session.query(User).filter(User.user_id==seller_id).first()
    seller=db.session.query(Seller).filter(Seller.seller_id==seller_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], password)

    if is_pass_correct:
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.phone=phone
        seller.shop_name=shop_name
        seller.shop_url=shop_url

        db.session.commit()
        response=jsonify({"message": "User Successfully updated"})
        response.status_code = 200
        return response
    response = jsonify({"message": "Incorrect Password"})
    response.status_code = 400
    return response

def change_password(seller_id, old_password, new_password):
    user=db.session.query(User).filter(User.user_id==seller_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], old_password)

    if is_pass_correct:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        response=jsonify({"message": "User Successfully updated"})
        response.status_code = 200
        return response
    response = jsonify({"message": "Incorrect Password"})
    response.status_code = 400
    return response

def retrieve_products_by_seller(id):
    seller=db.session.query(Seller).filter(Seller.seller_id==id).first()
    if not seller:
        return {"message": "Seller not found"}, 404
    products=db.session.query(Product).filter(Product.seller_id==id).all()
    product_schema=ProductSchema(many=True)
    product_output = product_schema.dump(products)
    return product_output

def retrieve_consultations_by_seller(id):
    seller=db.session.query(Seller).filter(Seller.seller_id==id).first()
    if not seller:
        return {"message": "Seller not found"}, 404
    consultations=db.session.query(Consultation).filter(Product.seller_id==id).all()
    consultation_schema=ConsultationSchema(many=True)
    consultation_output = consultation_schema.dump(consultations)
    return consultation_output
