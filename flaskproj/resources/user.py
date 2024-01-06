from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_smorest import abort
from flaskproj.db import db
from flaskproj.models.user import UserModel
from flaskproj.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required

blp = Blueprint("user", __name__, description="Operations on user")


@blp.route("/user/<string:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user


@blp.route("/user")
class UserList(MethodView):

    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        try:
            user = UserModel(name=user_data["name"],
                             password=pbkdf2_sha256.hash(user_data["password"]))
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="User with this name already exists"
            )
        return user


@blp.route("/login", methods=["POST"])
class LoginUser(MethodView):

    @blp.arguments(UserSchema(only=["name", "password"]), as_kwargs=True)
    def post(self, name, password):
        user = UserModel.query.filter_by(name=name).first()

        if user and pbkdf2_sha256.verify(password, user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        else:
            abort(401, message="Invalid username or password")
