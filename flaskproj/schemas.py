from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(load_only=True)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Int(required=False)


class CategoryQuerySchema(Schema):
    user_id = fields.Int(required=False)


class RecordQuerySchema(Schema):
    user_id = fields.Int(required=True)
    category_id = fields.Str()


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    sum = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
