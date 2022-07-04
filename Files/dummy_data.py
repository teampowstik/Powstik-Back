from faker import Faker
from random import randint
import json

fake=Faker()

#create a json of 20 users with random id, first name,last name, email, phone, user_type, password
def create_users():
    users=[]
    for i in range(20):
        user={
            "first_name":fake.first_name(),
            "last_name":fake.last_name(),
            "email":fake.email(),
            "phone":fake.phone_number(),
            "password":"helloworld",
            "is_seller":False
        }
        users.append(user)
    return users

#create a json of 20 products with random id, quantity, image link, description, price, discount, effective price, category, related products id
def create_products():
    products=[]
    names=["Food Superior","Food Elevate","Meal Luxuriate","Meal Region","Healthy Palace","Healthy Cuisine","Food Micro","Foodoont","Food Stable","Healthy Paramount",
"Food Clever","Food Utopia","Healthyops","Meal Owl","Healthy Edge","Food Natural","Food Hideaway","Food Connection","Healthy Motivate","Food Lane"]    
    for i in range(20):
        product={
            "name":names[i],
            "qty_left":randint(1,100),
            "image":fake.image_url(),
            "description":fake.text(),
            "price":randint(1,100),
            "discount":randint(1,100),
            "category":fake.random_element(elements=("Metabolics","Diabetes","MotherAndChild")),
            "related_products":fake.random_element(elements=(randint(1,100),randint(1,100),randint(1,100)))
        }
        products.append(product)
    return products

#create a json of 20 sellers with random id, shop name, shop url
def create_sellers():
    sellers=[]
    for i in range(20):
        seller={
            "first_name":fake.first_name(),
            "last_name":fake.last_name(),
            "email":fake.email(),
            "phone":fake.phone_number(),
            "password":"helloworld",
            "is_seller":True,
            "shop_name":fake.company(),
            "shop_url":fake.url()
        }
        sellers.append(seller)
    return sellers

#create a json of 20 consultations with random id, consultation, image link, description, price, discount, effective price, category, related products id
def create_consultations():
    consultations=[]
    for i in range(20):
        names=[
"Health Crew","Health Aid","Health Elevate","Health Viva","Health Nurture","Health Breathe","Health Skill","Health Younger","Breathe Fortify",
"Breathe Flourish","Breathe Refresh","Breathe Check","Breathe Prime","Breathe Connect",'Breathe Health','Life Mass','Life Heroic','Life Active',
'Life Legion','Life Repair']
        consultation={
            "consultation":names[i],
            "consultant":fake.name(),
            "image":fake.image_url(),
            "description":fake.text(),
            "availability":fake.random_element(elements=("Available","Not Available")),
            "cost":randint(1,100),
            "discount":randint(1,100),
            "category":fake.random_element(elements=("Metabolics","Diabetes","MotherAndChild")),
            "related":fake.random_element(elements=(randint(1,20),randint(1,20),randint(1,20))),
            "bio_data":fake.text()
        }
        consultations.append(consultation)
    return consultations

users=create_users()
products=create_products()

#convert users to json
users_json=json.dumps(users)
#convert products to json
products_json=json.dumps(products)
#convert sellers to json
sellers_json=json.dumps(create_sellers())
#convert consultations to json
consultations_json=json.dumps(create_consultations())

with open('Files\\user\\users.json', 'w') as fp: 
    print(users_json, file=fp)

with open('Files\\product\\products.json', 'w') as fp: 
    print(products_json, file=fp)

with open('Files\\seller\\sellers.json', 'w') as fp: 
    print(sellers_json, file=fp)

with open('Files\\consultations\\consultations.json', 'w') as fp: 
    print(consultations_json, file=fp)
