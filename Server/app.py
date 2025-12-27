from flask import Flask
import logging
import sys
import socket

from routes.index_routes import index_bp
from routes.run_script_routes import run_script_bp
from routes.create_script_routes import create_script_bp
from routes.settings_route import settings_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(run_script_bp)
app.register_blueprint(create_script_bp)
app.register_blueprint(settings_bp)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "0.0.0.0"

def run_flask():
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
