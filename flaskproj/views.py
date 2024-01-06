import os
from flaskproj import app
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flaskproj.db import db
from flaskproj.resources.user import blp as UserBlueprint
from flaskproj.resources.category import blp as CategoryBlueprint
from flaskproj.resources.record import blp as RecordBlueprint

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Finance REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = '/swagger_ui'
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = "jose"
db.init_app(app)

api = Api(app)

jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"message": "The token has expired.", "error": "token_expired"}


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"message": "Signature verification failed.", "error": "invalid_token"}


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }


with app.app_context():
    db.create_all()

api.register_blueprint(UserBlueprint)
api.register_blueprint(CategoryBlueprint)
api.register_blueprint(RecordBlueprint)
