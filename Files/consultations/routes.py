from flask import Blueprint, request, jsonify
from .utils import AllConsultations, AddConsultation, RemoveConsultation, UpdateConsultation, ConsultationByCategory, ConsultationByID, check_consultation_seller_relation, check_is_seller
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin, CORS
from pydantic import ValidationError

consultation_blueprint = Blueprint('consultation', __name__, url_prefix='/consultation')
cors = CORS(consultation_blueprint, resources={r"/foo": {"origins": "*"}})

@consultation_blueprint.get('/')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetConsultations():
    result = AllConsultations()
    if not result:
        response = jsonify({'message': 'No consultations found'})

        return response, 204
    return result

@consultation_blueprint.get('/<int:consultation_id>')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetConsultationsbyID(consultation_id):
    result = ConsultationByID(consultation_id)
    if result is None:
        response={}
        return response, 204
    response = jsonify(result)
    return response, 200

@consultation_blueprint.get('bycategory/<string:category>')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetConsultbyCategory(category):
    try:
        result = ConsultationByCategory(category)
        if result is None:
            response={}
            return response, 204
        return result
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400

@consultation_blueprint.post('/')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def NewConsultation():
    try:
        if request.is_json:
            seller_id = get_jwt_identity()  
            res = request.get_json()
            res['seller_id'] = seller_id
            response = AddConsultation(**res)
            return response, response.status_code
        response = jsonify({"message": "Request must be JSON"})
        return response, 415
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400

@consultation_blueprint.patch('/<int:consultation_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchConsultation(consultation_id):
    try:
        if request.is_json:
            seller_id = get_jwt_identity()  
            res = request.get_json()
            res['consultation_id'] = consultation_id
            res['seller_id']=seller_id
            response = UpdateConsultation(**res)
            return response, response.status_code

        response = jsonify({"message": "Request must be JSON"})
        return response, 415
    except ValidationError as err:
        response = jsonify({'message': err.errors()})
        return response, 400
        

@consultation_blueprint.delete('/<int:consultation_id>')
@jwt_required()
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteConsultation(consultation_id):
    if request.is_json:
        seller_id = get_jwt_identity()
        result=RemoveConsultation(consultation_id,seller_id)
        if result:
            response = result
            return response
        else:
            response = jsonify({"message": "You are not authorized to delete this consultation"})
            response.status_code = 401
            return response
    response = jsonify({"message": "Request must be JSON"})
    response.status_code = 415
    return response