from flask import request, jsonify, Blueprint
from Files import db
from ..models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.post('/')
def add_user():
    if request.is_json:
        user=User(first_name=request.json['first_name'],last_name=request.json['last_name'],
                email=request.json['email'],password = request.json['password'],
                phone = request.json['phone'],user_type = request.json['user_type'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User Successfully Added"}, 201

    return {"message": "Request must be JSON"}, 415

@user.get('/')
def get_user():
    user_details = user.query.all()
    return jsonify(user_details)

@user.get('/<int:id>')
def get_user(id):
    user_details=db.session.query(User).filter(User.user_id==id).first()
    if not user_details:
        return {"message": "User not found"}, 404
    return jsonify(user_details)

@user.delete("/delete/<int:user_id>")
def delete_user(user_id):
    user_details=db.session.query(User).filter(User.user_id==user_id).first()
    if not user_details:
        return {"message": "Unable to find user"}, 404
    db.session.delete(user_details)
    db.session.commit()
    return {"message": "User Successfully Registered"}, 201


