from . import db, marshl # noqa
from .models import Post, User # noqa



class UserModelsSchema(marshl.Schema): # noqa
	class Meta: # noqa
		fields = ('id', 'fullName', 'username', 'email') # noqa

user_models_schema = UserModelsSchema()
users_models_schema = UserModelsSchema(many=True)


class PostModelsSchema(marshl.Schema): # noqa
	class Meta: # noqa
		fields = ('id', 'post_title', 'post_subtitle', 'post_content','user_id','created_date') # noqa

post_models_schema = PostModelsSchema()
posts_models_schema = PostModelsSchema(many=True)
