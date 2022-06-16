import json
from flask import Blueprint, request, jsonify
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory

consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation_blueprint.get('/')
def GetConsultations():
    result = AllConsultations()
    if not result:
           return {"message": "There are 0 consultations"}, 200
    return jsonify(result), 200

@consultation_blueprint.get('bycategory')
def GetConsultbyCategory():
    result = ConsultationByCategory(
        request.json["category"]
        )
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

@consultation_blueprint.patch('/')
def PatchConsultation():
    if request.is_json:
        result =  UpdateConsultation(
            request.json["consultation_id"],
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
        

@consultation_blueprint.delete('/')
def DeleteConsultation():
    if request.is_json:
        RemoveConsultation(
            request.json["consultation_id"]
        )
        return {"message": "Deleted Consultation"}
    return {"message": "Request must be JSON"}, 415
