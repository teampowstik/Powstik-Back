from flask import request, jsonify
from Files import db
from ..models import User, Seller, UserSchema, SellerSchema, UserSellerSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import or_

def login_user(email, password):
    user=db.session.query(User).filter(User.email==email).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        is_pass_correct = check_password_hash(output["password"], password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=output["user_id"])
            access = create_access_token(identity=output["user_id"])

            return jsonify({"status" : "logged in" , "access_token": access, "refresh_token": refresh})
        return "Incorrect Password"

    return "User Credentials Incorrect"


def register_user(first_name, last_name, email, password, phone, user_type, shop_name, shop_url):

    user=db.session.query(User).filter(or_(User.email==email,User.phone==phone)).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        return {"message": "Phone or Email already exists"}, 409
    
    password = request.json.get('password')
    pwd_hash = generate_password_hash(password)

    user=User(first_name=first_name,last_name=last_name, email=email,password = pwd_hash, phone = phone, user_type = user_type)
    db.session.add(user)
    user_id=db.session.query(User).filter(User.email==email).first().user_id
    seller=Seller(shop_name=shop_name, shop_url=shop_url, seller_id=user_id)
    db.session.add(seller)
    db.session.commit()
    return {"message" : "Seller Added"}, 201
    
def retrieve_all_users():
    user_seller=db.session.query(User,Seller).join(Seller,User.user_id==Seller.seller_id).all()
    user_seller_schema=UserSellerSchema(many=True)
    output = user_seller_schema.dump(user_seller)
    print(output)
    return output



def retrieve_user_byID(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    seller_details=db.session.query(Seller).filter(Seller.seller_id==user_id).first()
    if not user_details or not seller_details:
        return {"message": "User not found"}, 404
    user_schema=UserSchema()
    output_user = user_schema.dump(user_details)
    seller_schema=SellerSchema()
    output_seller = seller_schema.dump(seller_details)
    return jsonify({"user": output_user, "seller": output_seller})

def remove_user(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    seller_details=db.session.query(Seller).filter(Seller.seller_id==user_id).first()
    if not user_details or not seller_details:
        return None
    db.session.delete(user_details)
    db.session.delete(seller_details)
    db.session.commit()
    return {"message": "User Successfully deleted"}, 201

def update_user(user_id, first_name, last_name, email, password, phone, shop_name, shop_url):
    user=db.session.query(User).filter(User.user_id==user_id).first()
    seller=db.session.query(Seller).filter(Seller.seller_id==user_id).first()
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
        return {"message": "User Successfully updated"}, 201        
    
    return "Incorrect Password"

def change_password(user_id, old_password, new_password):
    user=db.session.query(User).filter(User.user_id==user_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], old_password)

    if is_pass_correct:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return {"message": "User Password Successfully changed"}, 201        

    return "Incorrect Password"