from app import app, api, mongo, jwt
from flask import request
import os, sys, re, uuid
from datetime import datetime, date, timedelta, timezone
from config import Config
from functools import wraps
import random, time, string
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jti

#DATABASE collections
users = mongo.db.Users #User details
products = mongo.db.Products #Products collection
orders = mongo.db.Orders #Created orders
cart = mongo.db.Cart #User's carts
jwt_blacklist = mongo.db.JWT_Blacklist #Revoked jwts


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = jwt_blacklist.find_one({"jti": jti})
    return token is not None

#Nigerian time
def stamp():
    return str(datetime.now(timezone.utc) + timedelta(hours=1))

# decorator function frequesting api key as header
def token_required(f):
    @wraps(f)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return {"status": False, "message": "Token is missing at " + request.url, "data": None}, 401

        if token == Config.API_KEY:
            return f(*args, **kwargs)
        else:
            return {"status": False, "message": "Invalid token at " + request.url, "data": None}, 401

    return decorated

def is_valid_email(email):
    #regex pattern to check for valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
