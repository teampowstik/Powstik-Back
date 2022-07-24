from flask import jsonify
from Files import db
from ..models import User, UserSchema, Cart, CartSchema
import razorpay

def make_payments_utils(user_id):

    cart = Cart.query.filter_by(customer_id=user_id, item_type='cart').all()
    cart_schema = CartSchema(many=True)
    result = cart_schema.dump(cart)
    payment_amount=0

    for item in result:
        payment_amount+=item["item_total"]

    client = razorpay.Client(auth=("rzp_test_UJ7AxMRWbVx9IE", "o5RHoEZeMpEkEHbhjH5PX9t4"))
    payment = client.order.create({'amount': payment_amount*100, 'currency': 'INR', 'payment_capture': '1'})
    return payment
    # return render_template('pay.html', payment=payment)

