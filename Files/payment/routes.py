from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from razorpay import Payment
from .utils import make_payments_utils

from flask_cors import cross_origin, CORS

payment = Blueprint('payment', __name__, url_prefix='/payment')
cors = CORS(payment, resources={r"/foo": {"origins": "*"}})

@payment.get('/')
@jwt_required()
def make_payment():
    user_id = get_jwt_identity()
    
    if user_id is None:
        response = jsonify({"message": "Invalid User"})
        return response, 404

    response = make_payments_utils(user_id)

    return response