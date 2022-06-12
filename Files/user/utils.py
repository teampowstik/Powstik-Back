from flask import request, jsonify
from Files import db
from ..models import User, UserSchema

def add_new_user():
    if request.is_json:
        user=User(first_name=request.json['first_name'],last_name=request.json['last_name'],
                email=request.json['email'],password = request.json['password'],
                phone = request.json['phone'],user_type = request.json['user_type'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User Successfully Added"}, 201

    return {"message": "Request must be JSON"}, 415

def retrieve_all_users():
    user_details = User.query.all()
    user_schema=UserSchema(many=True)
    output = user_schema.dump(user_details)
    return jsonify(output)

def retrieve_user_byID(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return {"message": "User not found"}, 404
    user_schema=UserSchema()
    output = user_schema.dump(user_details)
    return jsonify(output)

def remove_user(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return {"message": "Unable to find user"}, 404
    db.session.delete(user_details)
    db.session.commit()
    return {"message": "User Successfully deleted"}, 201