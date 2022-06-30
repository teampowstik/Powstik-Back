import json
from unittest import result
from flask import Blueprint, request, jsonify, make_response
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory, ConsultationByID, check_consultation_seller_relation, check_is_seller
from flask_jwt_extended import jwt_required, get_jwt_identity

consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation_blueprint.get('/')
def GetConsultations():
    result = make_response(AllConsultations())
    if not result:
           return {"message": "There are 0 consultations"}, 204
    result.headers['Access-Control-Allow-Origin'] = '*'
    return result, 200

@consultation_blueprint.get('/<int:consultation_id>')
def GetConsultationsbyID(consultation_id):
    result = ConsultationByID(consultation_id)
    if result is None:
        return {}, 204
    return jsonify(result), 200

@consultation_blueprint.get('bycategory/<string:category>')
def GetConsultbyCategory(category):
    result = ConsultationByCategory(category)
    if result is None:
           return {"message": "There are 0 consultations under this category"}, 204
    return jsonify({"result": result}), 200 #json.dumps(result)

@consultation_blueprint.post('/')
@jwt_required()
def NewConsultation():
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        if res['seller_id'] == seller_id:
            result = AddConsultation(**res)
            return jsonify({"result": result}), 200
        else:
            return {"message": "You are not the seller"}, 400
    return {"message": "Request must be JSON"}, 415

@consultation_blueprint.patch('/<int:consultation_id>')
@jwt_required()
def PatchConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        res['consultation_id'] = consultation_id
        if res['seller_id']==seller_id:  
            result = UpdateConsultation(**res)
            return jsonify({"result": result}), 200
        else:
            return {"message": "You are not the seller"}, 400
    return {"message": "Request must be JSON"}, 415
        

@consultation_blueprint.delete('/<int:consultation_id>')
@jwt_required()
def DeleteConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        result=RemoveConsultation(consultation_id,seller_id)
        return jsonify({"result": result}), 200
    return {"message": "Request must be JSON"}, 415
