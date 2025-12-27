from flask import Blueprint, render_template
from Config.config import Config

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def index():
    return render_template('index.html', script_count = len(Config.saved_scripts))
