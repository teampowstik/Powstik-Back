import json
from flask import Blueprint, request, jsonify
from .utils import get_all_consultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory

consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation_blueprint.get('/')
def get_consultations():
    result = get_all_consultations()
    if not result:
           return {"message": "There are 0 consultations"}, 200
    return jsonify(result), 200

@consultation_blueprint.get('bycategory/<string:category>')
def GetConsultbyCategory(category):
    result = ConsultationByCategory(category)
    if result is None:
           return {"message": "There are 0 consultations under this category"}, 204
    return json.dumps(result), 200

@consultation_blueprint.post('/')
def NewConsultation():
    if request.is_json:
        result = AddConsultation(
            request.json['consultation'], 
            request.json['consultant'], 
            request.json['description'], 
            request.json['availability'], 
            request.json['image'], 
            request.json['cost'], 
            request.json['discount'], 
            request.json['related'], 
            request.json['bio_data'], 
            request.json['categories'],
            request.json['seller_id']
            )
        return result
    
    return {"message": "Request must be JSON"}, 415

@consultation_blueprint.patch('/<int:id>')
def PatchConsultation(id):
    if request.is_json:
        result =  UpdateConsultation(
            id,
            request.json['consultation'],
            request.json['consultant'],
            request.json['description'],
            request.json['availability'],
            request.json['image'],
            request.json['cost'],
            request.json['discount'],
            request.json['related'],
            request.json['bio_data'],
            request.json['categories'] #csv of category_names
        )
        return result
    return {"message": "Request must be JSON"}, 415
        

@consultation_blueprint.delete('/<int:id>')
def DeleteConsultation(id):
    if request.is_json:
        RemoveConsultation(
            id
        )
        return {"message": "Deleted Consultation"}
    return {"message": "Request must be JSON"}, 415
