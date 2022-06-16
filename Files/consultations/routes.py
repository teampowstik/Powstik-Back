import json
from flask import Blueprint, request, jsonify
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory, ConsultationByID

consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation_blueprint.get('/')
def GetConsultations():
    result = AllConsultations()
    if not result:
           return {"message": "There are 0 consultations"}, 200
    return jsonify(result), 200

@consultation_blueprint.get('/<int:consultation_id>')
def GetConsultationsbyID(consultation_id):
    result = ConsultationByID(consultation_id)
    if result is None:
        return {}, 204
    return jsonify(result), 200
    return

@consultation_blueprint.get('bycategory/<string:category>')
def GetConsultbyCategory(category):
    result = ConsultationByCategory(category)
    if result is None:
           return {"message": "There are 0 consultations under this category"}, 204
    return json.dumps(result), 200

@consultation_blueprint.post('/')
def NewConsultation():
    if request.is_json:
        res = request.get_json()
        result = AddConsultation(**res)
        return result
    
    return {"message": "Request must be JSON"}, 415

@consultation_blueprint.patch('/<int:consultation_id>')
def PatchConsultation(consultation_id):
    if request.is_json:
        res = request.get_json()
        res['consultation_id'] = consultation_id
        result = UpdateConsultation(**res)
        return result
    return {"message": "Request must be JSON"}, 415
        

@consultation_blueprint.delete('/<int:consultation_id>')
def DeleteConsultation(consultation_id):
    if request.is_json:
        RemoveConsultation(consultation_id)
        return {"message": "Deleted Consultation"}
    return {"message": "Request must be JSON"}, 415
