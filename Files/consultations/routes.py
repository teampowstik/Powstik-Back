from flask import Blueprint, request, jsonify
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory, ConsultationByID, check_consultation_seller_relation, check_is_seller
from flask_jwt_extended import jwt_required, get_jwt_identity


consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')

@consultation_blueprint.get('/')
def GetConsultations():
    result = AllConsultations()
    if not result:
        response = jsonify({'message': 'No consultations found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@consultation_blueprint.get('/<int:consultation_id>')
def GetConsultationsbyID(consultation_id):
    result = ConsultationByID(consultation_id)
    if result is None:
        response={}
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@consultation_blueprint.get('bycategory/<string:category>')
def GetConsultbyCategory(category):
    result = ConsultationByCategory(category)
    if result is None:
        response={}
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response = jsonify({"result": result})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@consultation_blueprint.post('/')
@jwt_required()
def NewConsultation():
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        if res['seller_id'] == seller_id:
            response = AddConsultation(**res)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, response.status_code
        else:
            response = jsonify({"message": "You are not authorized to add this consultation"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@consultation_blueprint.patch('/<int:consultation_id>')
@jwt_required()
def PatchConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()  
        res = request.get_json()
        res['consultation_id'] = consultation_id
        if res['seller_id']==seller_id:  
            response = UpdateConsultation(**res)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, response.status_code
        else:
            response = jsonify({"message": "You are not authorized to update this consultation"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
    response = jsonify({"message": "Request must be JSON"})
    return response, 415
        

@consultation_blueprint.delete('/<int:consultation_id>')
@jwt_required()
def DeleteConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        result=RemoveConsultation(consultation_id,seller_id)
        if result:
            response = result
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, response.status_code
        else:
            response = jsonify({"message": "You are not authorized to delete this consultation"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 401
    response = jsonify({"message": "Request must be JSON"})
    return response, 415