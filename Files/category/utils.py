from Files import db
from ..models import BelongsToCategory, BelongsToCategorySchema
from flask import jsonify

def AllCategories():
    result = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id==None).all()
    output = BelongsToCategorySchema(many=True).dump(result)
    return {"result":output}

def AddCategory(category_name):
    try:
        #check if category already exists
        result = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name==category_name).first()
        if result:
            return {'message': 'Category Already Exists'}
        result = BelongsToCategory(category_name = category_name, pro_con_id = None)
        db.session.add(result)
        db.session.commit()
        response=jsonify({"message":"Category Added"})
        response.status_code = 201
        return response
    except:
        response=jsonify({"message":"Caty Not Added"})
        response.status_code = 400
        return response


def UpdateCategoryName(name, new_name):
    result = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name==name).first()
    if result:
        result.category_name = new_name
        db.session.commit()
        response=jsonify({
            'message': 'Category Name Patched',
            'category-name': new_name
        })
        response.status_code = 200
        return response
    else:
        response=jsonify({"message":"Category Does Not Exist"})
        response.status_code = 400
        return response

def RemoveCategoryRecord(CategoryName):
    try:
        records = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name==CategoryName).all()
        for record in records:
            if record:
                db.session.delete(record)
        db.session.commit()
        return True
    except:
        return False

    