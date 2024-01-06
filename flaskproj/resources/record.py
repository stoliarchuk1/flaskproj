from flask_smorest import Blueprint
from flask.views import MethodView
from flask_smorest import abort
from flaskproj.db import db
from sqlalchemy.exc import IntegrityError
from flaskproj.models.record import RecordModel
from flaskproj.models.category import CategoryModel
from flaskproj.models.user import UserModel
from flaskproj.schemas import RecordSchema, RecordQuerySchema

blp = Blueprint("record", __name__, description="Operations on record")


@blp.route("/record/<string:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        return record


@blp.route("/record")
class RecordList(MethodView):

    @blp.arguments(RecordQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, RecordSchema(many=True))
    def get(self, **kwargs):
        user_id = kwargs.get("user_id")

        if not user_id:
            return abort(400, message="Need at least user id to get record")

        if user_id:
            query = db.session.query(RecordModel).filter_by(user_id=user_id)

        category_id = kwargs.get("category_id")

        if category_id:
            query = db.session.query(RecordModel).filter_by(user_id=user_id).filter_by(category_id=category_id)

        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def post(self, record_data):
        if not db.session.query(db.exists().where(UserModel.id == record_data["user_id"])).scalar():
            abort(
                400,
                message="This user are not exist"
            )
        if not db.session.query(db.exists().where(CategoryModel.id == record_data["category_id"])).scalar():
            abort(
                400,
                message="This category are not exist"
            )
        else:
            record = RecordModel(**record_data)

            try:
                db.session.add(record)
                db.session.commit()
            except IntegrityError:
                abort(
                    400,
                    message="Error while creating record"
                )
            return record
