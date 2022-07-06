from flask import request, jsonify
from Files import db
from ..models import User, UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

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
        response=jsonify({"message": "User Successfully updated"})
        response.status_code = 201
        return response
    response=jsonify({"message": "Incorrect Password"})
    response.status_code = 401
    return response

def change_password(user_id, old_password, new_password):
    user=db.session.query(User).filter(User.user_id==user_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], old_password)

    if is_pass_correct:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        response=jsonify({"message": "User Successfully updated"})
        response.status_code = 201
        return response
    response=jsonify({"message": "Incorrect Password"})
    response.status_code = 401
    return response
