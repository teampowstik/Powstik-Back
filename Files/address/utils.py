from flask import request, jsonify
from Files import db
from ..models import Address, AddressSchema, User, UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import or_

def add_address_util(user_id, line1, line2, city, state, country, zipcode, password):

    user=db.session.query(User).filter(User.user_id==user_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    is_pass_correct = check_password_hash(output["password"], password)

    if is_pass_correct:
        address = Address(line1=line1, line2=line2, city=city, state=state, country=country, zipcode=zipcode, user_id=user_id)
        db.session.add(address)
        db.session.commit()
        return {"message": "Address added"}, 201

    return {"message": "Incorrect Password"}, 401

def retrieve_all_addresses():
    address_details = Address.query.all()
    address_schema=AddressSchema(many=True)
    output = address_schema.dump(address_details)
    return {"result":output}

def retrieve_address_byUserID(user_id):
    address_details=db.session.query(Address).filter(Address.user_id==user_id).first()
    if not address_details:
        return {"message": "Address not found for this user"}, 204
    address_schema=AddressSchema()
    output = address_schema.dump(address_details)
    return output

def remove_address(user_id,address_id):
    address_details=db.session.query(Address).filter(Address.address_id==address_id).first()
    if not address_details:
        return {"message": "Address not found"}, 204
    address_schema=AddressSchema()
    output = address_schema.dump(address_details)
    if output["user_id"]==user_id:
        db.session.delete(address_details)
        db.session.commit()
        return {"message": "Address removed"}, 201
    return {"message": "Address and user details do not match"}, 204

def update_address_util(user_id,address_id,line1,line2,city,state,country,zipcode):
    address_details=db.session.query(Address).filter(Address.address_id==address_id).first()
    if not address_details:
        return {"message": "Address not found"}, 204
    address_schema=AddressSchema()
    output = address_schema.dump(address_details)
    if output["user_id"]==user_id:
        address_details.line1=line1
        address_details.line2=line2
        address_details.city=city
        address_details.state=state
        address_details.country=country
        address_details.zipcode=zipcode
        db.session.commit()
        return {"message": "Address updated"}, 201
    return {"message": "Address and user details do not match"}, 204