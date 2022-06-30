from flask import Blueprint, request, jsonify
from .utils import AllCategories, AddCategory, UpdateCategoryName, RemoveCategoryRecord


category_blueprint = Blueprint("category", __name__, url_prefix="/category")

@category_blueprint.get('/') #get all categories
def GetAllCategories():
    result = AllCategories()
    if result is None:
           return {"message": "There are 0 categories. Add one!"}, 204
    return jsonify(result), 200

@category_blueprint.post('/') #adding a new category
def PostAddCategory():
    if request.is_json:
        category_name=request.json["category_name"]
        result = AddCategory(category_name)
        return result
    return {"message": "Request must be JSON"}, 415

@category_blueprint.patch('/<string:name>')
def PatchName(name):
    if request.is_json:
        new_name = request.json['category_name']
        res = UpdateCategoryName(name, new_name)
        return res
    return {"message": "Request must be JSON"}, 415

@category_blueprint.delete('/')
def DeleteName():
    if request.is_json:
        CategoryName = request.json['category_name']
        result = RemoveCategoryRecord(CategoryName)
        if result:
            return {'message': 'Removed All Records with Category name'}, 201
        else:
            return {'message': 'Request Error'}, 400
    return {"message": "Request must be JSON"}, 415
    