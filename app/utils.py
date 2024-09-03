from app import app, api, mongo
from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
import os, sys, re, uuid
from datetime import datetime, date, timedelta
from config import Config
from functools import wraps
import random, time, string

#DATABASE collections
users = mongo.db.Users #User details
products = mongo.db.Products #Products collection
orders = mongo.db.Orders #Created orders
cart = mongo.db.Cart #User's carts

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