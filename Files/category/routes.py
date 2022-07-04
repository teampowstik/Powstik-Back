from flask import Blueprint, request, jsonify
from .utils import AllCategories, AddCategory, UpdateCategoryName, RemoveCategoryRecord


category_blueprint = Blueprint("category", __name__, url_prefix="/category")

@category_blueprint.get('/') #get all categories
def GetAllCategories():
    result = AllCategories()
    if result is None:
        response = jsonify({'message': 'No categories found'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 204
    response =  jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@category_blueprint.post('/') #adding a new category
def PostAddCategory():
    if request.is_json:
        category_name=request.json["category_name"]
        result = AddCategory(category_name)
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@category_blueprint.patch('/<string:name>')
def PatchName(name):
    if request.is_json:
        new_name = request.json['category_name']
        res = UpdateCategoryName(name, new_name)
        response = res
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    response = jsonify({"message": "Request must be JSON"})
    return response, 415

@category_blueprint.delete('/')
def DeleteName():
    if request.is_json:
        CategoryName = request.json['category_name']
        result = RemoveCategoryRecord(CategoryName)
        if result:
            response = jsonify({"message": "Category deleted"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            response = jsonify({'message': 'Request Error'})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 400
    response = jsonify({"message": "Request must be JSON"})
    return response, 415    