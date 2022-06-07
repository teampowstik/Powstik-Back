from faker import Faker
from random import randint
import json

fake=Faker()

#create a json of 100 users with random id, first name,last name, email, phone, user_type, password
def create_users():
    users=[]
    for i in range(100):
        user={
            "user_id":i,
            "first_name":fake.first_name(),
            "last_name":fake.last_name(),
            "email":fake.email(),
            "phone":fake.phone_number(),
            "user_type":fake.random_element(elements=("customer","seller","consultant")),
            "password":fake.password()
        }
        users.append(user)
    return users

#create a json of 100 products with random id, quantity, image link, description, price, discount, effective price, category, related products id
def create_products():
    products=[]
    for i in range(100):
        product={
            "product_id":i,
            "name":fake.name(),
            "qty_left":randint(1,100),
            "image":fake.image_url(),
            "description":fake.text(),
            "price":randint(1,100),
            "discount":randint(1,100),
            "effective_price":randint(1,100),
            "category":fake.random_element(elements=("Metabloics","Geriatrics","Mother and Child")),
            "related_products":fake.random_element(elements=(randint(1,100),randint(1,100),randint(1,100)))
        }
        products.append(product)
    return products

users=create_users()
products=create_products()

#convert users to json
users_json=json.dumps(users)
#convert products to json
products_json=json.dumps(products)


with open('users.json', 'w') as fp: 
    print(users_json, file=fp)

with open('products.json', 'w') as fp: 
    print(products_json, file=fp)

