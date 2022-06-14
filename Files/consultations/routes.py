from flask import Blueprint, request, jsonify
from .utils import get_all_consultations, ConsultationByCategory, AddConsultation

consultation = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation.get('/')
def get_consultations():
    result = get_all_consultations()
    if result is None:
           return {"message": "There are 0 consultations"}, 204
    return jsonify(result), 200

@consultation.get('/category/<int:id>')
def GetConsultbyCategory(id):
    result = ConsultationByCategory(id)
    if result is None:
           return {"message": "There are 0 consultations under this category"}, 204
    return jsonify(result), 200

@consultation.post('/')
def NewConsultation():
    if request.is_json:
        consultation_id = request.json['consultation_id']
        consultation = request.json['consultation']
        description = request.json['description']
        availability = request.json['availability']
        image = request.json['image']
        cost = request.json['cost']
        discount = request.json['discount']
        related = request.json['related']
        bio_data = request.json['bio_data']
        category_ids = request.json['category'] #csv of c_ids
        result =  AddConsultation(consultation_id, consultation, description, 
                        availability, image, cost, discount, related, bio_data, category_ids)
        return result
    
    return {"message": "Request must be JSON"}, 415
