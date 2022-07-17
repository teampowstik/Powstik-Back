from Files import db
from ..models import BelongsToCategory, BelongsToCategorySchema, Category, CategorySchema
from flask import jsonify
from pydantic import HttpUrl, validate_arguments

def AllCategories():
    result = db.session.query(Category).all()
    output = CategorySchema(many=True).dump(result)
    return {"result":output}

@validate_arguments
def AddCategory(category_name:str,description:str,image:HttpUrl):
    try:
        #check if category already exists
        result = db.session.query(Category).filter(Category.category_name==category_name).first()
        if result:
            response=jsonify({"message":"Category Already Exists"})
            response.status_code = 400 
            return response
        result = Category(category_name = category_name, description = description, image = image)
        db.session.add(result)
        db.session.commit()
        response=jsonify({"message":"Category Added"})
        response.status_code = 201
        return response
    except:
        response=jsonify({"message":"Category Not Added"})
        response.status_code = 400
        return response

@validate_arguments
def UpdateCategoryName(name:str, new_name:str, description:str, image:HttpUrl):
    result = db.session.query(Category).filter(Category.category_name==
                                                            name).first()
    if result:
        result.category_name = new_name
        result.description = description
        result.image = image
        db.session.commit()
        response=jsonify({
            'message': 'Category Name Patched'
        })
        response.status_code = 200
        return response
    else:
        response=jsonify({"message":"Category Does Not Exist"})
        response.status_code = 400
        return response

@validate_arguments
def RemoveCategoryRecord(CategoryName:str):
    try:
        category=db.session.query(Category).filter(Category.category_name==CategoryName).first()
        records = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_id==category.category_id).all()
        for record in records:
            if record:
                db.session.delete(record)
        db.session.delete(category)
        db.session.commit()
        return True
    except:
        return False

    