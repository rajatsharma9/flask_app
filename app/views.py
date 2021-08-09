from . import db # noqa
from .models import Post,User
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_restful import Resource, Api, reqparse
from .schema import users_models_schema, posts_models_schema


main = Blueprint('main', __name__)
api = Api(main)


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('post_title',type=str, help='Title is Required', required=True) 
user_post_args.add_argument('post_subtitle',type=str, help='SubTitle is Required', required=True)
user_post_args.add_argument('post_content',type=str, help='Content is Required', required=True)
user_post_args.add_argument('user_id',type=str, help='User Id is Required', required=True)


@main.route('/')
def home():
    """Show the Home Page for users."""
    return render_template('home.html')


@main.route('/about')
def about():
    """Show the loged in user post."""
    return render_template('about.html')


class PostCrudOprations(Resource):
    """Here we create API to perform CRUD oprations for user post."""

    def get(self, **kwargs):
        post_object = Post.query.all()
        json_post_object = posts_models_schema.dump(post_object)
        return jsonify(json_post_object)

    def post(self, **kwargs):
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
        return "Data Submitted Successful"

    def put(self, post_id):
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
        return "Data updated Successful"

    def delete(self, post_id):
        post_object = Post.query.filter_by(id=post_id).first()
        db.session.delete(post_object)
        db.session.commit()
        return "Data delete Successful"

api.add_resource(PostCrudOprations,'/user_post/<int:post_id>')




