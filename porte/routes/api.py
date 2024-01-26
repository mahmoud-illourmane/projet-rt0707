from app import app, DATABASE_NAME, MONGO_URI          
from flask import jsonify, request
import json, base64, datetime
from pymongo.errors import PyMongoError

"""
|
|   This file contains the REST API of the door simulation routes for the project.
|
|   Author: Mahmoud ILLOURMANE
|   Date: December 26, 2024
|
"""

"""
|   ===============
|   API REST ROUTES
|   ===============
"""

