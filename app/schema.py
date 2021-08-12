from . import db, marshl # noqa
from .models import Post, User # noqa
from marshmallow import fields, Schema, validates, ValidationError # noqa


class UserModelsSchema(marshl.Schema): # noqa
	class Meta: # noqa
		fields = ('id', 'fullName', 'username', 'email') # noqa

user_models_schema = UserModelsSchema()
users_models_schema = UserModelsSchema(many=True)


class SigninFields(Schema): # noqa
	fullName = fields.String(required=True) # noqa
	username = fields.String(required=True) # noqa
	email = fields.Email(required=True) # noqa
	password = fields.String(required=True) # noqa

	@validates('username')
	def validate_email(self,username):
		user_object = User.query.filter_by(username=username).first()
		if user_object:
			raise ValidationError('A username already exists.')

	@validates('email')
	def validate_email(self,email):
		user_object = User.query.filter_by(email=email).first()
		if user_object:
			raise ValidationError('A user already exists with this email address.')

	@validates('password')
	def validate_password(self, password):
		if len(password) <= 8:
			raise ValidationError('Password Length must be eight digit.')

class LoginSchema(Schema):
	email = fields.Email(required=True)
	password = fields.String(required=True)

	@validates('email')
	def validate_email_password(self,email):
		user_object = User.query.filter_by(email=email).first()
		if not user_object:
			raise ValidationError('Invalid email address.')

	