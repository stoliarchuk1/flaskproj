from flaskproj.db import db
from sqlalchemy.sql import func


class RecordModel(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=False,
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        unique=False,
        nullable=False
    )

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    sum = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")
