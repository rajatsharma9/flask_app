from . import db, marshl # noqa
from .models import Post, User # noqa



class UserModelsSchema(marshl.Schema): # noqa
	class Meta: # noqa
		fields = ('id', 'fullName', 'username', 'email') # noqa

user_models_schema = UserModelsSchema()
users_models_schema = UserModelsSchema(many=True)
