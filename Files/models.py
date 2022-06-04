
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)

class User (db.Model):
    __tablename__ = "User"
    user_id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(20),nullable=False)
    last_name=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    phone=db.Column(db.String(10),unique=True,nullable=False)
    user_type=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"User('{self.user_id}','{self.first_name}','{self.user_type}')"

class Cart (db.Model):
    __tablename__ = 'Cart'
    table_sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id=db.Column(db.Integer, db.ForeignKey(db.ForeignKey("User.user_id")))
    price=db.Column(db.Numeric(10,2),nullable=False)
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))
    quantity=db.Column(db.Integer,nullable=False)
    item_type=db.Column(db.String(20),nullable=False) # cart item or wishlist item 
    item_total = db.Column(db.Numeric(10,2),nullable=False) # price * qty
    
    def __repr__(self):
        return f"User('{self.customer_id}')"

class Seller (db.Model):
    __tablename__ = 'Seller'
    seller_id=db.Column(db.Integer, db.ForeignKey("User.user_id"),primary_key=True)
    shop_name=db.Column(db.String(20),nullable=False)
    shop_url=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"User('{self.seller_id}','{self.shop_name}')"

class Consultant (db.Model):
    __tablename__ = 'Consultant'
    consultant_id=db.Column(db.Integer, db.ForeignKey("User.user_id"),primary_key=True)
    consultation_domain=db.Column(db.String(20),nullable=False)
    cost=db.Column(db.Numeric(10,2),nullable=False)

    def __repr__(self):
        return f"User('{self.consultant_id}','{self.cost}')"

class Address (db.Model):
    __tablename__ = 'Address'
    address_id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String(80), nullable=False)
    line2 = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(db.ForeignKey("User.user_id")))
    
class Order (db.Model):
    __tablename__ = "Order"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    address_id = db.Column(db.Integer, db.ForeignKey("Address.address_id"))
    amount = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime(timezone=True), server_default = func.now())
    customer_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))
    
class Order_Items(db.Model):
    __tablename__ = "OrderItems"
    table_sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("Order.order_id"))
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))
    
class Category (db.Model):
    __tablename__ = 'Category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    category_name = db.Column(db.String, nullable=False)
    
class BelongsToCategory (db.Model):
    __tablename__ = "BelongsToCategoryRel"
    table_sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'))
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))

class Product (db.Model):
    __tablename__ = 'Product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    qty_left = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable = False)
    discount = db.Column(db.Integer, nullable = False)
    effective_price = db.Column(db.Integer, nullable = False)
    category = db.Column(db.Integer, db.ForeignKey('Category.category_id'))
    related_products = db.Column(db.String, nullable=True)  

class Sells (db.Model):
    __tablename__ = "Sells"
    table_sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    seller_id = db.Column(db.Integer, db.ForeignKey("Seller.seller_id"))
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))
class Trending (db.Model): 
    __tablename__ = "Trending"
    trending_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))
    
    
class Coupons (db.Model):
    __tablename__ = "Coupons"
    coupon_id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    used = db.Column(db.String(5), nullable=False)
    minimum_cart_value = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("Cart.cart_id"), nullable=True)

class Reviews (db.Model):
    __tablename__ = "Reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(80), nullable=False)
    review_for = db.Column(db.String(10), nullable=False)
    pro_con_id = db.Column(db.Integer, 
                           db.ForeignKey("Consultant.consultant_id"), 
                           db.ForeignKey("Product.product_id"))