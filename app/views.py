from . import db # noqa
from .models import Post, User
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_restful import Resource, Api
from .schema import users_models_schema

main = Blueprint('main', __name__)
api = Api(main)


class GetAllUsers(Resource):
    """Shows a list of all Users."""

    def get(self):
        """."""
        user = User.query.all()
        result = users_models_schema.dump(user)
        return jsonify(result)

api.add_resource(GetAllUsers, '/hello')


@main.route('/')
def home():
    """Show the Home Page for users."""
    return render_template('home.html')


@main.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """Here we use Http methods for creating our post by using forms."""
    if request.method == 'POST':
        data = {
            'post_title': request.form['title'],
            'post_subtitle': request.form['subtitle'],
            'post_content': request.form['content'],
        }
        post_object = Post(data)
        post_object.user_id = current_user.id
        db.session.add(post_object)
        db.session.commit()
    return render_template('createPost.html')


@main.route('/show_all_post/<int:user_id>')
def user_post(user_id):
    """Here we get/show the all Post of user by user_id."""
    user_posts = Post.query.filter(Post.user_id == user_id).order_by(
        Post.created_date.desc()).all()

    return render_template('showAllPost.html', user_posts=user_posts)


@main.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Here we use Http methods for updating the Post when user clickon update button."""
    update_post_object = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        update_post_object.post_title = post_title
        update_post_object.post_content = post_content
        db.session.add(update_post_object)
        db.session.commit()
        return redirect(
            url_for('main.user_post', user_id=update_post_object.user_id)
        )

    return render_template('update.html', user_post=update_post_object)


@main.route('/delete_post/<int:post_id>')
def delete(post_id):
    """Here we delete the Post when user click on delete button."""
    user_post_object = Post.query.filter_by(id=post_id).first()
    db.session.delete(user_post_object)
    db.session.commit()
    return redirect(url_for('main.user_post', user_id=user_post_object.user_id))


@main.route('/about')
def about():
    """Show the loged in user post."""
    return render_template('about.html')
