from email.policy import HTTP
from unittest import result
from flask import Blueprint, jsonify, request
from .utils import add_new_user, retrieve_all_users, retrieve_user_byID, remove_user, update_user
from ..models import User, UserSchema, Seller, SellerSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from Files import db


user = Blueprint('user', __name__, url_prefix='/seller')

@user.post('/register')
def register():
    password = request.json.get('password')
    pwd_hash = generate_password_hash(password)

    user=User(first_name=request.json['first_name'],last_name=request.json['last_name'],
                email=request.json['email'],password = pwd_hash,
                phone = request.json['phone'],user_type = request.json['user_type'])
    seller=Seller(shop_name=request.json['shop_name'],shop_url=request.json['shop_url'])
    
    db.session.add(user)
    db.session.add(seller)
    db.session.commit()
    # return {"message": "User Successfully Added"}, 201
    return jsonify({
        'message': 'Seller Successfully Added',
        'password': pwd_hash,
        'old password': password
    }), 201


@user.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user=db.session.query(User).filter(User.email==email).first()
    user_schema=UserSchema()
    output = user_schema.dump(user)

    if output:
        is_pass_correct = check_password_hash(output["password"], password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=output["user_id"])
            access = create_access_token(identity=output["user_id"])

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'email': output["email"],
                    'entered password' : password,
                    'hashed passord' : output["password"],
                }
            })

        return jsonify("Incorrect Password"), 401

    return jsonify("User Credentials Incorrect"), 404

@user.post('/')
def post_user():
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        user_type = request.json.get('user_type')
        add_new_user(first_name, last_name, email, password, phone, user_type)
        return {"message": "User Successfully Added"}, 201
    return {"message": "Request must be JSON"}, 415
    # return add_new_user()

@user.patch('/<int:user_id>')
def patch_user(user_id):
    if request.is_json:
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')
        user_type = request.json.get('user_type')
        res=update_user(user_id, first_name, last_name, email, password, phone, user_type)
        if res is None:
            return {"message": "User not found"}, 404
        return {"message": "User Successfully Updated"}, 200
    return {"message": "Request must be JSON"}, 415

@user.get('/')
def get_users():
    result = retrieve_all_users()
    if result is None:
        return jsonify({'message': 'No users found'}), 404
    return jsonify(result)

@user.get('/<int:user_id>')
def get_user_byID(user_id):
    result = retrieve_user_byID(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 404
    return jsonify(result)

@user.delete("/<int:user_id>")
def delete_user(user_id):
    result = remove_user(user_id)
    if result is None:
        return jsonify({'message': 'No user found'}), 404
    return result