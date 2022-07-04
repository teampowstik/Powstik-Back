from flask import request, jsonify
from Files import db
from ..models import User, UserSchema
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
        return {"message":"Incorrect Password"}, 401

    return {"message":"User not found"}, 204

def register_user(first_name, last_name, email, password, phone):

    user=db.session.query(User).filter(or_(User.email==email,User.phone==phone)).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        return {"message": "Phone or Email already exists"}, 409
    
    password = request.json.get('password')
    if (len(password)<=6 or len(password)>=20):
        return {"message": "Password must be between 6 and 20 characters"}, 400
    pwd_hash = generate_password_hash(password)

    user=User(first_name=first_name,last_name=last_name, email=email,password = pwd_hash, phone = phone, is_seller = False)

    db.session.add(user)
    db.session.commit()
    
    return {"message" : "User Registered as Customer"}, 201
    
def retrieve_all_users():
    user_details = User.query.all()
    user_schema=UserSchema(many=True)
    output = user_schema.dump(user_details)
    return {"result":output}

def retrieve_user_byID(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return {"message": "User not found"}
    user_schema=UserSchema()
    output = user_schema.dump(user_details)
    return output

def remove_user(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return None
    db.session.delete(user_details)
    db.session.commit()
    return {"message": "User Successfully deleted"}, 201

def update_user(user_id, first_name, last_name, email, password, phone):
    user=db.session.query(User).filter(User.user_id==user_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], password)

    if is_pass_correct:
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.phone=phone

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