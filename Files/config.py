from dotenv import load_dotenv
import os

import jwt

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
COMMON_DB=os.getenv('COMMON_DB')

class Config(object):
    SECRET_KEY=SECRET_KEY
    SQLALCHEMY_DATABASE_URI = COMMON_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'