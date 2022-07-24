from flask import request, jsonify
from Files import db
from ..models import User, UserSchema, Seller
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import or_
from pydantic import EmailStr, validate_arguments

@validate_arguments
def login_user(email:EmailStr, password:str):
    user=db.session.query(User).filter(User.email==email).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        is_pass_correct = check_password_hash(output["password"], password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=output["user_id"])
            access = create_access_token(identity=output["user_id"])
            response=jsonify({"message": "User Successfully logged in", "refresh": refresh, "access": access, "is_seller": output["is_seller"]})
            response.status_code = 200
            return response
        response=jsonify({"message": "Login Failed. Please check your email and password"})
        response.status_code = 401
        return response
    response=jsonify({"message": "Login Failed. Please check your email and password"})
    response.status_code = 401
    return response

@validate_arguments
def register_user(first_name:str, last_name:str, email:EmailStr, password:str, phone:int, is_seller:bool):
    user=db.session.query(User).filter(or_(User.email==email,User.phone==phone)).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        response=jsonify({"message": "User already exists"})
        response.status_code = 409
        return response
    
    password = request.json.get('password')
    if (len(password)<=6 or len(password)>=20):
        response=jsonify({"message": "Password must be between 6 and 20 characters"})
        response.status_code = 400
        return response
    pwd_hash = generate_password_hash(password)

    user=User(first_name=first_name,last_name=last_name, email=email,password = pwd_hash, phone = phone, is_seller = is_seller)
    db.session.add(user)
    if is_seller:
        seller_user_id=db.session.query(User).filter(User.email==email).first().user_id
        seller=Seller(seller_id=seller_user_id,shop_name="",shop_url="")
        db.session.add(seller)

    db.session.commit()
    
    response=jsonify({"message": "User Successfully registered"})
    response.status_code = 201
    return response
    