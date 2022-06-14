from flask import jsonify
from Files import db
from ..models import Consultation, ConsultationSchema 
from ..models import BelongsToCategory, BelongsToCategorySchema

def get_all_consultations():
    result = Consultation.query.all()
    consultation_schema = ConsultationSchema(many=True)
    output = consultation_schema.dump(result)
    return output
        
def ConsultationByCategory(category_id):
    initial = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id==category_id).all()
    result = []
    for init in initial:
        consultation_schema = ConsultationSchema(many=False)
        temp = consultation_schema.dump(init)
        temp = jsonify(temp)
        consultation = db.session.query(Consultation).filter(Consultation.consultation_id==temp["pro_con_id"]).first()
        consultation_schema = ConsultationSchema(many=False)
        consultation = consultation_schema.dump(consultation)
        result.append(jsonify(consultation))
    return result

def AddConsultation(consultation_id, consultation, description, availability, 
                    image, cost, discount, related, bio_data, CategoryIDs):
    try:   
        consultation = Consultation(consultation_id = consultation_id, consultation = consultation, 
                                    description = description, availability=availability, 
                                    image=image, cost=cost, discount=discount, related=related, bio_data=bio_data
                                    )
        for CategoryID in CategoryIDs.split(","):
            temp = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_id == CategoryID).first()
            BTCSchema = BelongsToCategory(many=False)
            temp = BTCSchema.dump(temp)
            BelongsTo = BelongsToCategory(category_id = CategoryID, 
                                        category_name = temp["category_name"], 
                                        pro_con_id = consultation_id)
            db.session.add(BelongsTo)
        db.session.add(consultation)
        db.session.commit()
    except:
        return {"message: Consultation not added", 400}
    return {"message": "Done"}, 201