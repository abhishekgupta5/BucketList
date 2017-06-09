# app/auth/__init__.py

from flask import Blueprint()

#Instance of a blueprint that represents the auth blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views
