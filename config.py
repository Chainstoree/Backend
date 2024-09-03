import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# creating a configuration class
class Config(object):
    MONGO_URI =  os.environ.get('MONGO_URI') 
    #BASE_URL = os.environ.get('BASE_URL')
    APP_ENV = os.environ["APP_ENVIRONMENT"]
    API_KEY = os.environ["API_KEY"]
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']