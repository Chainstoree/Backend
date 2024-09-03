import os
from dotenv import load_dotenv
from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_cors import CORS


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#Initialise Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
CORS(app)
api = Api(app)
mongo = PyMongo(app=app, uri=Config.MONGO_URI)

from app import endpoints