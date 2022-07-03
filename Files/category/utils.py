from Files import db
from ..models import BelongsToCategory, BelongsToCategorySchema

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
        return {'message': 'Category Added Successfully.'}, 200
    except:
        return { 'message': 'Category not added.'}, 400


def UpdateCategoryName(name, new_name):
    result = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name==
                                                            name).first()
    if result:
        result.category_name = new_name
        db.session.commit()
        return {
            'message': 'Category Name Patched',
            'category-name': new_name
        }
    else:
        return {'message': 'Category Not Found'}

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

    