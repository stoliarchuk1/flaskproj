from flaskproj.db import db


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        unique=False,
        nullable=True
    )

    record = db.relationship(
        "RecordModel",
        back_populates="category",
        lazy="dynamic",
    )

    user = db.relationship("UserModel", back_populates="category")
