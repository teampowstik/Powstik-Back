import json
from flask import Blueprint, request, jsonify
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory, ConsultationByID, check_consultation_seller_relation, check_is_seller
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin


consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

CORS(consultation_blueprint)

consultation_blueprint.config['CORS_HEADERS'] = 'Content-Type'

@consultation_blueprint.get('/')
@cross_origin()
def GetConsultations():
    result = make_response(AllConsultations())
    if not result:
           return {"message": "There are 0 consultations"}, 204
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
@jwt_required()
def NewConsultation():
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        res['seller_id'] = seller_id
        result = AddConsultation(**res)
        return result
    
    return {"message": "Request must be JSON"}, 415

@consultation_blueprint.patch('/<int:consultation_id>')
@jwt_required()
def PatchConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        res['consultation_id'] = consultation_id
        res['seller_id']=seller_id
        result = UpdateConsultation(**res)
        return result
    return {"message": "Request must be JSON"}, 415
        

@consultation_blueprint.delete('/<int:consultation_id>')
@jwt_required()
def DeleteConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        res=RemoveConsultation(consultation_id,seller_id)
        return res
    return {"message": "Request must be JSON"}, 415
