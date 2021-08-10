from . import db # noqa
from .models import Post
from flask import Blueprint, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from .schema import posts_models_schema


main = Blueprint('main', __name__)
api = Api(main)


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('post_title', type=str, help='Title is Required', required=True)
user_post_args.add_argument('post_subtitle', type=str, help='SubTitle is Required', required=True)
user_post_args.add_argument('post_content', type=str, help='Content is Required', required=True)
user_post_args.add_argument('user_id', type=str, help='User Id is Required', required=True)


@main.route('/')
def home():
    """Show the Home Page for users."""
    return render_template('home.html')


@main.route('/about')
def about():
    """Show the loged in user post."""
    return render_template('about.html')


class PostList(Resource):
    """."""

    def get(self, **kwargs):
        """."""
        post_object = Post.query.all()
        json_post_object = posts_models_schema.dump(post_object)
        return jsonify(json_post_object)

    def post(self, **kwargs):
        """."""
        post_dict = user_post_args.parse_args()
        data = {
            'post_title': post_dict['post_title'],
            'post_subtitle': post_dict['post_subtitle'],
            'post_content': post_dict['post_content'],
        }
        post_object = Post(data)
        post_object.user_id = post_dict['user_id']
        db.session.add(post_object)
        db.session.commit()
        return {"messge": "Data Submitted Successful", "Data": data, "status": "200 OK"}


api.add_resource(PostList, '/user_post')


class PostResource(Resource):
    """Here we create API to perform CRUD oprations for user post."""

    def get(self, post_id):
        """."""
        post_object = Post.query.filter_by(id=post_id).all()
        json_post_object = posts_models_schema.dump(post_object)
        return jsonify(json_post_object)

    def put(self, post_id):
        """."""
        post_dict = user_post_args.parse_args()
        post_title = post_dict['post_title']
        post_subtitle = post_dict['post_subtitle']
        post_content = post_dict['post_content']
        update_post_object = Post.query.filter_by(id=post_id).first()
        update_post_object.post_title = post_title
        update_post_object.post_subtitle = post_subtitle
        update_post_object.post_content = post_content
        db.session.add(update_post_object)
        db.session.commit()
        return {"message": "Data updated Successful", "updated_data": post_dict, "status": "201 ok"}

    def delete(self, post_id):
        """."""
        post_object = Post.query.filter_by(id=post_id).first()
        db.session.delete(post_object)
        db.session.commit()
        return {"message": "Data delete Successful", "status": "201 ok"}

api.add_resource(PostResource, '/user_post/<int:post_id>')
