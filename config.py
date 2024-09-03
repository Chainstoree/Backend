import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# creating a configuration class
class Config(object):
    
    MONGO_URI =  os.environ.get('MONGO_URI') 
    BASE_URL = os.environ.get('BASE_URL')
    APP_ENVIRONMENT = os.environ["APP_ENVIRONMENT"]
    API_KEY = os.environ["API_KEY"]