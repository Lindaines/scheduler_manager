from flask import Flask, Blueprint
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

import settings
from app.error_handlers import configuration as config_error_handlers
from app.restplus import configuration as config_resplus
from app.midlewares import configuration as config_middlewares
from app.routes import import_routes
from app.cli import configuration as config_cli

# Initialize Flask
app = Flask(__name__, static_folder="static")
app.url_map.strict_slashes = False
blueprint = Blueprint("api", __name__, url_prefix=None)

# Proxy
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configuration Cors
CORS(app, resources={r"/*": {"origins": "*"}})

# Load configuration
app.config.from_object(settings.load_config())

# Configuration Cli
config_cli(app=app)

# Initialize Restplus and import Routes
config_resplus(app=app, blueprint=blueprint)
import_routes()

# Configuration Middlewares and Error Handlers
config_middlewares(app=app)
config_error_handlers(app=app)
