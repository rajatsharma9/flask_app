from . import db, marshl # noqa
from .models import Post, User # noqa
from marshmallow import fields, Schema


class UserModelsSchema(marshl.Schema): # noqa
	class Meta: # noqa
		fields = ('id', 'fullName', 'username', 'email') # noqa

user_models_schema = UserModelsSchema()
users_models_schema = UserModelsSchema(many=True)

class SigninFields(Schema):
	fullName = fields.Str(required=True)
	username = fields.Str(required=True)
	email = fields.Str(required=True)
	password = fields.Str(required=True)

	class Meta: # noqa
		fields = ('id', 'fullName', 'username', 'email') # noqa

user_models_schema = UserModelsSchema()
users_models_schema = UserModelsSchema(many=True)
