from flask import jsonify
from Files import db
from ..models import User, UserSchema,Product, ProductSchema, BelongsToCategory, BelongsToCategorySchema, Category
from pydantic import HttpUrl, validate_arguments

def check_product_seller_relation(product_id, seller_id):
    result=db.session.query(Product).filter(Product.product_id==product_id).filter(Product.seller_id==seller_id).first()
    if not result:
        return False
    return True

def check_is_seller(seller_id):
    result=db.session.query(User).filter(User.user_id==seller_id).first()
    user_schema=UserSchema()
    output = user_schema.dump(result)
    if output["is_seller"] == True:
        return True
    return False    

def get_all_products():
    result=Product.query.all()
    response=[]
    for product in result:
        output=jsonify(ProductSchema(many=False).dump(product))
        output=output.get_json()
        categories=db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="P"+str(output["product_id"]))
        output["categories"] = []
        for category in categories:
            id=category.category_id
            res=db.session.query(Category).filter(Category.category_id==id).first()
            output["categories"].append(res.category_name)
        response.append(output)

    response=jsonify({"result":response})
    response.status_code=200
    return response

@validate_arguments
def products_by_category(category_name:str):
    category_name=category_name.lower()
    category=db.session.query(Category).filter(Category.category_name==category_name).first()
    if not category:
        response=jsonify({"message": "Category does not exist"})
        response.status_code=400
        return response
    records = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_id==category.category_id).filter(BelongsToCategory.pro_con_id.startswith('P')).all()
    result = []
    for record in records:
        output = jsonify(
            BelongsToCategorySchema(many=False).dump(record)
        )
        output= output.get_json()
        output = output["pro_con_id"]
        output = int(output[1:])
        temp = db.session.query(Product).filter(Product.product_id==output).first()
        product = ProductSchema(many=False).dump(temp)
        result.append(
            jsonify(product).get_json()
        )
    response=jsonify({"result":result})
    response.status_code=200
    return response
    
def get_product_by_id(id):
    result = db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        return None
    categories=db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="P"+str(id))
    result = ProductSchema(many=False).dump(result)
    result["categories"] = []
    for category in categories:
        id=category.category_id
        res=db.session.query(Category).filter(Category.category_id==id).first()
        result["categories"].append(res.category_name)
    return result

@validate_arguments
def add_product(name:str, description:str, price:float, image:HttpUrl, discount:float, qty_left:int, categories:str, vendor_info:str, seller_id:int):
    
    if check_is_seller(seller_id) == False:
        response=jsonify({"message": "You are not a seller"})
        response.status_code=400
        return response

    result = db.session.query(Product).filter(Product.name==name).filter(Product.seller_id==seller_id).first()
    if result:
        response=jsonify({"message": "Product already exists"})
        response.status_code=400
        return response
    #1. Adding Product
    record=Product(name=name,description=description,price=price,image=image,
                    discount=discount,effective_price=float(price)-(float(discount)*float(price)/100),
                    qty_left=qty_left,vendor_info=vendor_info,seller_id=seller_id)
    db.session.add(record)
    
    #2. Getting Prod ID
    
    temp = db.session.query(Product).filter(Product.name==name).filter(Product.seller_id==seller_id).first()
    output = ProductSchema(many=False).dump(temp)
    product_id = jsonify(output).json["product_id"]
    product_id = "P" + str(product_id)
        
    #3. Adding Categories
    categories = categories.replace(" ","")
    categories=categories.split(",")
    for CategoryName in categories:
        CategoryName=CategoryName.lower()
        category=db.session.query(Category).filter(Category.category_name==CategoryName).first()
        if category:
            record=BelongsToCategory(pro_con_id=product_id,category_id=category.category_id)
            db.session.add(record)
        else:
            response=jsonify({"message": "Category does not exist"})
            response.status_code=400
            return response
    
    db.session.commit()
    response=jsonify({"message": "Product added successfully"})
    response.status_code=201
    return response

@validate_arguments
def update_product(product_id:int, name:str, description:str, price:float, image:HttpUrl, discount:float, qty_left:int, categories:str, vendor_info:str, seller_id:int):
    
    if check_is_seller(seller_id) == False:
        response=jsonify({"message": "You are not a seller"})
        response.status_code=400
        return response

    if check_product_seller_relation(product_id, seller_id) == False:
        response=jsonify({"message": "You are not the seller of this product"})
        response.status_code=400
        return response

    product=db.session.query(Product).filter(Product.product_id==product_id).first()
    if not product:
        response=jsonify({"message": "Product does not exist"})
        response.status_code=204
        return response
    
    #1. Update product table
    product.name=name
    product.description=description
    product.price=price
    product.image=image
    product.discount=discount
    product.effective_price=float(price)-(float(discount)*float(price)/100)
    product.qty_left=qty_left
    product.vendor_info=vendor_info
    db.session.commit()
    
    #2. Delete Current Product Category Mapping
    records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="P"+str(product_id))
    for record in records:
        db.session.delete(record)
    
    # 3. Adding new Product Category Mapping
    product_id = "P" + str(product_id)
    categories = categories.replace(" ","")
    categories=categories.split(",")
    for CategoryName in categories:
        CategoryName=CategoryName.lower()
        category=db.session.query(Category).filter(Category.category_name==CategoryName).first()
        if category:
            record=BelongsToCategory(pro_con_id=product_id,category_id=category.category_id)
            db.session.add(record)
        else:
            response=jsonify({"message": "Category does not exist"})
            response.status_code=400
            return response

    db.session.commit()
    response=jsonify({"message": "Product updated successfully"})
    response.status_code=202
    return response

def remove_product(product_id, seller_id):

    if check_is_seller(seller_id) == False:
        response=jsonify({"message": "You are not a seller"})
        response.status_code=400
        return response

    if check_product_seller_relation(product_id, seller_id) == False:
        response=jsonify({"message": "You are not the seller of this product"})
        response.status_code=400
        return response

    product=db.session.query(Product).filter(Product.product_id==product_id).first()
    if not product:
        return None
    product_id = "P"+str(product_id)
    records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id==product_id).all()
    for record in records:
        db.session.delete(record)
    db.session.delete(product)
    db.session.commit()
    response=jsonify({"message": "Product removed successfully"})
    response.status_code=202
    return response