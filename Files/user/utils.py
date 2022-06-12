from flask import request, jsonify
from Files import db
from ..models import User, UserSchema

def add_new_user(first_name, last_name, email, password, phone, user_type):
    if request.is_json:
        user=User(first_name=first_name,last_name=last_name,email=email,password=password,phone=phone,user_type=user_type)
        db.session.add(user)
        db.session.commit()

def retrieve_all_users():
    user_details = User.query.all()
    user_schema=UserSchema(many=True)
    output = user_schema.dump(user_details)
    return output

def retrieve_user_byID(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return {"message": "User not found"}, 404
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

def update_user(user_id, first_name, last_name, email, password, phone, user_type):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return None
    user_details.first_name=first_name
    user_details.last_name=last_name
    user_details.email=email
    user_details.password=password
    user_details.phone=phone
    user_details.user_type=user_type

    db.session.commit()
    return {"message": "User Successfully updated"}, 201