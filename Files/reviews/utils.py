from flask import request, jsonify
from Files import db
from ..models import ReviewsSchema, Reviews

def retrieve_reviews_by_productID(pro_con_id):
    review_details = db.session.query(Reviews).filter(Reviews.pro_con_id==pro_con_id).all()
    if not review_details:
        return None
    review_schema=ReviewsSchema(many=True)
    output = review_schema.dump(review_details)
    return {"result":output}

def retrieve_reviews_by_userID(user_id):
    review_details = db.session.query(Reviews).filter(Reviews.user_id==user_id).all()
    if not review_details:
        return None
    review_schema=ReviewsSchema(many=True)
    output = review_schema.dump(review_details)
    return {"result":output}

def add_reviews(pro_con_id, user_id, rating, review, type):
    if type == 'product':
        pro_con_id = 'P' + str(pro_con_id)
    elif type == 'consultation':
        pro_con_id = 'C' + str(pro_con_id)
    
    review = Reviews(user_id=user_id, rating=rating, review=review, pro_con_id=pro_con_id)
    db.session.add(review)
    db.session.commit()
    return {"message": "Review added"}, 201