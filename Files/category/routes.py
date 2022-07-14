from flask import Blueprint, request, jsonify
from .utils import AllCategories, AddCategory, UpdateCategoryName, RemoveCategoryRecord
from flask_cors import cross_origin, CORS

category_blueprint = Blueprint("category", __name__, url_prefix="/category")
cors = CORS(category_blueprint, resources={r"/foo": {"origins": "*"}})

@category_blueprint.get('/') #get all categories
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def GetAllCategories():
    result = AllCategories()
    if result is None:
        response = jsonify({'message': 'No categories found'})

        return response, 204
    response =  jsonify(result)
    return response, 200

@category_blueprint.post('/') #adding a new category
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PostAddCategory():
    if request.is_json:
        category_name=request.json["category_name"]
        description=request.json["description"]
        image=request.json["image"]
        response = AddCategory(category_name.lower(),description,image)

        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@category_blueprint.patch('/<string:name>')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def PatchName(name):
    if request.is_json:
        new_name = request.json['new_name']
        description = request.json['description']
        image = request.json['image']
        res = UpdateCategoryName(name.lower(), new_name.lower(), description, image)
        response = res

        return response, response.status_code
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@category_blueprint.delete('/')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def DeleteName():
    if request.is_json:
        CategoryName = request.json['category_name']
        result = RemoveCategoryRecord(CategoryName.lower())
        if result:
            response = jsonify({"message": "Category deleted"})
    
            return response
        else:
            response = jsonify({'message': 'Request Error'})
    
            return response, 400
    response = jsonify({"message": "Request must be JSON"})
    return response, 415    