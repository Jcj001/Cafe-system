from flask import Blueprint
from .authentication import authentication
from .system_admin import admin
from .cafe_owner import owner
from .cafe_staff import staff
from .cafe_manager import manager

boundary = Blueprint('boundary', __name__, template_folder="templates", static_folder="assets")

# BLUEPRINTS REGISTRATION
boundary.register_blueprint(authentication)
boundary.register_blueprint(admin)
boundary.register_blueprint(owner)
boundary.register_blueprint(staff)
boundary.register_blueprint(manager)
