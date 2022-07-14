from flask import jsonify
from Files import db
from ..models import Consultation, ConsultationSchema, BelongsToCategory, BelongsToCategorySchema, Seller, User, UserSchema, Category, CategorySchema, Product, ProductSchema

def check_consultation_seller_relation(consultation_id, seller_id):
    result=db.session.query(Consultation).filter(Consultation.consultation_id==consultation_id).filter(Consultation.seller_id==seller_id).first()
    if not result:
        return False
    return True

def check_is_seller(seller_id):
    result=db.session.query(User).filter(User.user_id==seller_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(result)
    if output["is_seller"] == True:
        return True
    return False    

def AllConsultations():
    result = Consultation.query.all()
    consultation_schema = ConsultationSchema(many=True)
    output = consultation_schema.dump(result)
    return {"result":output}

def ConsultationByID(consultation_id):
    result = db.session.query(Consultation).filter(Consultation.consultation_id==consultation_id).first()
    if not result:
        return None
    categories=db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="C"+str(consultation_id))
    result = ConsultationSchema(many=False).dump(result)
    result["categories"] = []
    for category in categories:
        result["categories"].append(category.category_name)
    return result

def ConsultationByCategory(category_name):
    category_name=category_name.lower()
    category=db.session.query(Category).filter(Category.category_name==category_name).first()
    if not category:
        response=jsonify({"message": "Category does not exist"})
        response.status_code=400
        return response
    records = db.session.query(BelongsToCategory).filter(
        BelongsToCategory.category_id==category.category_id).filter(
            BelongsToCategory.pro_con_id!=None).filter(
                BelongsToCategory.pro_con_id.startswith('C')).all()
    result = []
    for record in records:
        output = jsonify(
            BelongsToCategorySchema(many=False).dump(record)
        )
        output= output.get_json()
        output = output["pro_con_id"]
        output = int(output[1:])
        temp = db.session.query(Consultation).filter(Consultation.consultation_id==output).first()
        consultation = ConsultationSchema(many=False).dump(temp)
        result.append(
            jsonify(consultation).get_json()
        )
    response=jsonify({"result":result})
    response.status_code=200
    return response

def AddConsultation(consultation, consultant, description, availability, 
                    image, cost, discount, related, bio_data, categories, seller_id):
    try:   
        if check_is_seller(seller_id) == False:
            response=jsonify({"message":"You are not a seller"})
            response.status_code=400
            return response
        result = db.session.query(Consultation).filter(Consultation.consultation==
                                                       consultation).filter(Consultation.seller_id==
                                                                            seller_id).first()
        if result:
            response=jsonify({"message":"Consultation Already Exists"})
            response.status_code=400
            return response
        result = Consultation(consultation = consultation, consultant=consultant,
                                    description = description, availability=availability, 
                                    image=image, cost=cost, discount=discount, 
                                    effective_price=float(cost)-(float(discount)*float(cost)/100),
                                    related=related, bio_data=bio_data, seller_id=seller_id)
        db.session.add(result)
        #getting Consultation ID
        temp = db.session.query(Consultation).filter(Consultation.consultation==
                                                     consultation).filter(Consultation.consultant==consultant).first()
        output = ConsultationSchema(many=False).dump(temp)
        consultation_id = jsonify(output).json["consultation_id"]
        consultation_id = "C" + str(consultation_id)
        categories = categories.replace(" ","")
        categories = categories.split(",")
        for CategoryName in categories:
            CategoryName=CategoryName.lower()
            category=db.session.query(Category).filter(Category.category_name==CategoryName).first()
            if category:
                record=BelongsToCategory(pro_con_id=consultation_id,category_id=category.category_id)
                db.session.add(record)
            else:
                response=jsonify({"message": "Category does not exist"})
                response.status_code=400
                return response
        db.session.commit()
    except:
        response=jsonify({"message":"Consultation Not Added"})
        response.status_code=400
        return response
    response=jsonify({"message":"Consultation Added"})
    response.status_code=200
    return response

def UpdateConsultation(consultation_id, consultation, consultant, description, 
                        availability, image, cost, discount, related, bio_data, categories, seller_id):
    try:
        if check_is_seller(seller_id) == False:
            response=jsonify({"message":"You are not a seller"})
            response.status_code=400
            return response

        if check_consultation_seller_relation(consultation_id, seller_id) == False:
            response=jsonify({"message":"You are not the seller of this consultation"})
            response.status_code=400
            return response
        #1. Update Consultation Table
        result = db.session.query(Consultation).filter(Consultation.consultation_id==consultation_id).first()
        result.consultation = consultation
        result.consultant = consultant
        result.description = description
        result.availability = availability
        result.image = image
        result.cost =cost
        result.discount = discount
        result.related =related
        result.bio_data =bio_data
        db.session.commit()
        
        #2. Delete Records from BelongsToCategory
        records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="C"+str(consultation_id))
        for record in records:
            db.session.delete(record)
        
        #3. Adding new categories for the respective Consultation
        consultation_id = "C" + str(consultation_id)
        categories = categories.replace(" ","")
        categories=categories.split(",")
        for CategoryName in categories:
            CategoryName=CategoryName.lower()
            category=db.session.query(Category).filter(Category.category_name==CategoryName).first()
            if category:
                record=BelongsToCategory(pro_con_id=consultation_id,category_id=category.category_id)
                db.session.add(record)
            else:
                response=jsonify({"message": "Category does not exist"})
                response.status_code=400
                return response
        db.session.commit()
        response=jsonify({"message":"Consultation Updated"})
        response.status_code=200
        return response
    except:
        response=jsonify({"message":"Consultation Not Updated"})
        response.status_code=400
        return response
        
def RemoveConsultation(consultation_id,seller_id):
    try:
        output = db.session.query(Consultation).filter(Consultation.consultation_id==consultation_id).first()
        if output is None:
            response=jsonify({"message":"Consultation Does Not Exist"})
            response.status_code=400
            return response

        if check_is_seller(seller_id) == False:
            response=jsonify({"message":"You are not a seller"})
            response.status_code=400
            return response

        if check_consultation_seller_relation(consultation_id, seller_id) == False:
            response=jsonify({"message":"You are not the seller of this consultation"})
            response.status_code=400
            return response

        db.session.delete(output)
        db.session.commit()
        records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="C"+str(consultation_id))
        for record in records:
            db.session.delete(record)
        db.session.commit()
        response=jsonify({"message":"Consultation Removed"})
        response.status_code=200
        return response
    except:
        response=jsonify({"message":"Consultation Not Removed"})
        response.status_code=400
        return response