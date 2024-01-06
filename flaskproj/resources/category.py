import flask
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_smorest import abort
from flaskproj.db import db
from sqlalchemy.exc import IntegrityError

from flaskproj.models import CategoryModel, UserModel
from flaskproj.schemas import CategorySchema, CategoryQuerySchema

blp = Blueprint("category", __name__, description="Operations on category")


@blp.route("/category/<string:category_id>")
class Category(MethodView):

    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category


@blp.route("/category")
class CategoryList(MethodView):

    @blp.arguments(CategoryQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, CategorySchema(many=True))
    def get(self, **kwargs):
        user_id = kwargs.get("user_id", None)

        if user_id is not None:
            categories = CategoryModel.query.filter_by(user_id=user_id).all()
        else:
            categories = CategoryModel.query.filter_by(user_id=None).all()

        return categories

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self, category_data):
        if not db.session.query(db.exists().where(UserModel.id == category_data["user_id"])).scalar():
            abort(
                400,
                message="This user are not exist"
            )
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Category with this name already exists"
            )
        return category
