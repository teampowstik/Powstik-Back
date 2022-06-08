from flask import Blueprint
from .utils import add_new_user, retrieve_all_users, retrieve_user_byID, delete_user

user = Blueprint('user', __name__, url_prefix='/user')

@user.post('/')
def post_user():
    return add_new_user()

@user.get('/')
def get_users():
    return retrieve_all_users()

@user.get('/<int:user_id>')
def get_user_byID(user_id):
    return retrieve_user_byID(user_id)

@user.delete("/delete/<int:user_id>")
def delete_user(user_id):
    return delete_user(user_id)

