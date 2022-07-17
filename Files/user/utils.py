from flask import jsonify
from Files import db
from ..models import User, UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import EmailStr, HttpUrl, validate_arguments

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

@validate_arguments
def update_user(user_id:int, first_name:str, last_name:str, email:EmailStr, phone:str, address:str, city:str, state:str, pincode:int, country:str, gender:str, plot_no:str, profile_img:HttpUrl):
    user=db.session.query(User).filter(User.user_id==user_id).first()

    user.first_name=first_name
    user.last_name=last_name
    user.email=email
    user.phone=phone
    user.address=address
    user.city=city
    user.state=state
    user.pincode=pincode
    user.country=country
    user.gender=gender
    user.plot_no=plot_no
    user.profile_img=profile_img

    db.session.commit()
    response=jsonify({"message": "User Successfully updated"})
    response.status_code = 201
    return response

@validate_arguments
def change_password(user_id:int, old_password:str, new_password:str):
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
