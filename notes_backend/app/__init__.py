from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
import os

# Attempt to load environment variables if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # It's optional; app will work without it if not installed.
    pass


app = Flask(__name__)

# Basic configuration with optional overrides from environment variables
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})

# OpenAPI / Swagger UI configuration
app.config["API_TITLE"] = os.getenv("API_TITLE", "Notes API")
app.config["API_VERSION"] = os.getenv("API_VERSION", "v1")
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"  # so it's available at /docs/openapi.json
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)
