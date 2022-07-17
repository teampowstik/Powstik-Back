import datetime
from flask import request, jsonify
from Files import db
from ..models import ReviewsSchema, Reviews,User, UserSchema
from sqlalchemy import func
from datetime import date


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

    review_date = date.today()
    
    review = Reviews(user_id=user_id, rating=rating, review=review, pro_con_id=pro_con_id)
    db.session.add(review)
    db.session.commit()
    return {"message": "Review added"}, 201

def get_reviews_with_user_utils(pro_con_id):
    review_details = db.session.query(Reviews).filter(Reviews.pro_con_id==pro_con_id).all()
    if not review_details:
        return None
    review_schema=ReviewsSchema(many=True)
    output = review_schema.dump(review_details)

    response=[]
    for item in output:
        user_details = db.session.query(User).filter(User.user_id==item["user_id"]).first()
        user_schema=UserSchema()
        user_output = user_schema.dump(user_details)
        item["user_details"]=user_output["first_name"]
        response.append(item)

    return output

def get_ratings_utils(pro_con_id):
    review_details = db.session.query(Reviews).filter(Reviews.pro_con_id==pro_con_id).all()
    if not review_details:
        return None
    review_schema=ReviewsSchema(many=True)
    output = review_schema.dump(review_details)

    response=[]
    no_of_responses=0
    total_rating=0
    star_count_5=0
    star_count_4=0
    star_count_3=0
    star_count_2=0
    star_count_1=0

    for item in output:
        no_of_responses+=1
        total_rating+=item["rating"]
        
        if item["rating"]==5:
            star_count_5+=1
        elif item["rating"]==4:
            star_count_4+=1
        elif item["rating"]==3:
            star_count_3+=1
        elif item["rating"]==2:
            star_count_2+=1
        elif item["rating"]==1:
            star_count_1+=1
    
    average_rating=total_rating/no_of_responses
    response = jsonify({"average_rating":average_rating,"no_of_verified_buyers": no_of_responses ,"star_count_5":star_count_5, "star_count_4":star_count_4, "star_count_3":star_count_3, "star_count_2":star_count_2, "star_count_1":star_count_1})
    # response.append({"average_rating":average_rating,"no_of_verified_buyers":no_of_responses,"star_count_5":star_count_5,"star_count_4":star_count_4,"star_count_3":star_count_3,"star_count_2":star_count_2,"star_count_1":star_count_1})
    return response