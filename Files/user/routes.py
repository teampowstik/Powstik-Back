from email.policy import HTTP
from flask import Blueprint, jsonify, request
from .utils import add_new_user, retrieve_all_users, retrieve_user_byID, remove_user
from ..models import User, UserSchema
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from Files import db


user = Blueprint('user', __name__, url_prefix='/user')

@user.post('/register')
def register():
    password = request.json.get('password')
    pwd_hash = generate_password_hash(password)

    user=User(first_name=request.json['first_name'],last_name=request.json['last_name'],
                email=request.json['email'],password = pwd_hash,
                phone = request.json['phone'],user_type = request.json['user_type'])
    
    db.session.add(user)
    db.session.commit()
    # return {"message": "User Successfully Added"}, 201
    return jsonify({
        'message': 'User Successfully Added',
        'password': pwd_hash,
        'old password': password
    }), 201


# @user.post('/login')
# def login():
#     email = request.json.get('email')
#     password = request.json.get('password')

#     user=db.session.query(User).filter(User.email==email).first()

#     if user:
#         is_pass_correct = check_password_hash(user.password, password)

#         if is_pass_correct:
#             refresh = create_refresh_token(identity=user.user_id)
#             access = create_access_token(identity=user.user_id)

#             return jsonify({
#                 'user': {
#                     'refresh': refresh,
#                     'access': access,
#                     'email': user.email,
#                 }
#             })

#         return jsonify({'password': user.password}), 401

#     return jsonify({'message': 'Invalid credentials'}), 401


@user.post('/')
def post_user():
    return add_new_user()


@user.get('/')
def get_users():
    return retrieve_all_users()


@user.get('/<int:user_id>')
def get_user_byID(user_id):
    return retrieve_user_byID(user_id)


@user.delete("/<int:user_id>")
def delete_user(user_id):
    return remove_user(user_id)
