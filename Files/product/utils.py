from flask_restful import reqparse
from flask import request, jsonify
from Files import db
from ..models import User, UserSchema,Product, ProductSchema, BelongsToCategory, BelongsToCategorySchema


add_product_args = reqparse.RequestParser()
add_product_args.add_argument('name', type=str, required=True, help='Product name cannot be blank!')
add_product_args.add_argument('description', type=str, required=True, help='Product description cannot be blank!')
add_product_args.add_argument('price', type=float, required=True, help='Product price cannot be blank!')
add_product_args.add_argument('image', type=str, required=True, help='Product image cannot be blank!')
add_product_args.add_argument('discount', type=float, required=True, help='Product discount cannot be blank!')
add_product_args.add_argument('qty_left', type=int, required=True, help='Product qty cannot be blank!')
add_product_args.add_argument('category', type=int, required=True, help='Product category cannot be blank!')
add_product_args.add_argument('related_products', type=str, required=True, help='Product related products cannot be blank!')

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
    product_schema=ProductSchema(many=True)
    output = product_schema.dump(result)
    return output

def products_by_category(category_name):
    records = db.session.query(BelongsToCategory).filter(
        BelongsToCategory.category_name==category_name).filter(
            BelongsToCategory.pro_con_id!=None).filter(
                BelongsToCategory.pro_con_id.startswith('P')).all()
    result = []
    for record in records:
        output = jsonify(
            BelongsToCategorySchema(many=False).dump(record)
        )
        output= output.get_json()
        output = output["pro_con_id"]
        output = int(output[1:])
        temp = db.session.query(Product).filter(Product.product_id==output).first()
        consultation = ProductSchema(many=False).dump(temp)
        result.append(
            jsonify(consultation).get_json()
        )
    return result
    
def get_product_by_id(id):
    result = db.session.query(Product).filter(Product.product_id==id).first()
    if not result:
        return None
    categories=db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="P"+str(id))
    result = ProductSchema(many=False).dump(result)
    result["categories"] = []
    for category in categories:
        result["categories"].append(category.category_name)
    return result

def add_product(name, description, price, image, discount, qty_left, categories, related_products, seller_id):
    
    if check_is_seller(seller_id) == False:
        return {"message": "You are not a seller"}, 400

    result = db.session.query(Product).filter(Product.name==name).filter(Product.seller_id==seller_id).first()
    if result:
        return {"message":"Product Already Exists"}
    #1. Adding Product
    record=Product(name=name,description=description,price=price,image=image,
                    discount=discount,effective_price=float(price)-(float(discount)*float(price)/100),
                    qty_left=qty_left,related_products=related_products,seller_id=seller_id)
    db.session.add(record)
    
    #2. Getting Prod ID
    
    temp = db.session.query(Product).filter(Product.name==name).filter(Product.seller_id==seller_id).first()
    output = ProductSchema(many=False).dump(temp)
    product_id = jsonify(output).json["product_id"]
    product_id = "P" + str(product_id)
        
    #3. Adding Categories
    
    for CategoryName in categories.split(","):
            temp = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name == CategoryName).first()
            if not temp is None:
                output = jsonify(
                    BelongsToCategorySchema(many=False).dump(temp)
                    )
                BelongsTo = BelongsToCategory(category_name = output.json["category_name"], 
                                            pro_con_id = product_id)
                db.session.add(BelongsTo)
            else:
                return {"message": "Wrong Category Entered"}, 400

    db.session.commit()
    
    db.session.commit()
    return {"message": "Done"}, 201

def update_product(product_id, name, description, price, image, discount, qty_left, categories, related_products, seller_id):
    
    if check_is_seller(seller_id) == False:
        return {"message": "You are not a seller"}, 400

    if check_product_seller_relation(product_id, seller_id) == False:
        return {"message": "You are not the seller of this product"}, 400

    product=db.session.query(Product).filter(Product.product_id==product_id).first()
    if not product:
        return {"message": "Product does not exist"}, 204
    
    #1. Update product table
    product.name=name
    product.description=description
    product.price=price
    product.image=image
    product.discount=discount
    product.effective_price=float(price)-(float(discount)*float(price)/100)
    product.qty_left=qty_left
    product.related_products=related_products
    db.session.commit()
    
    #2. Delete Current Product Category Mapping
    records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id=="P"+str(product_id))
    for record in records:
        db.session.delete(record)
    
    # 3. Adding new Product Category Mapping
    product_id = "P" + str(product_id)
    for CategoryName in categories.split(","):
        temp = db.session.query(BelongsToCategory).filter(BelongsToCategory.category_name == CategoryName).first()
        if not temp is None:
            output = jsonify(
                BelongsToCategorySchema(many=False).dump(temp)
                )
            BelongsTo = BelongsToCategory(category_name = output.json["category_name"], 
                                        pro_con_id = product_id)
            db.session.add(BelongsTo)
        else:
            return {"message": "Product Modified but Wrong Category(s) Entered"}, 400
    db.session.commit()

    return {"message": "Done"}, 202

def remove_product(product_id, seller_id):

    if check_is_seller(seller_id) == False:
        return {"message": "You are not a seller"}, 400

    if check_product_seller_relation(product_id, seller_id) == False:
        return {"message": "You are not the seller of this product. You cannot delete this product"}, 400

    product=db.session.query(Product).filter(Product.product_id==product_id).first()
    if not product:
        return None
    product_id = "P"+str(product_id)
    records = db.session.query(BelongsToCategory).filter(BelongsToCategory.pro_con_id==product_id).all()
    for record in records:
        db.session.delete(record)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Done"}