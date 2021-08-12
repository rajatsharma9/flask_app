from . import db # noqa
from .models import Post
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_jwt_extended import jwt_required


main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Show the Home Page for users."""
    return render_template('home.html')


@main.route('/create_post', methods=['POST'])
@jwt_required()
def create_post():
    """Here we use Http methods for creating our post by using forms."""
    if request.method == 'POST':
        user_login_data = request.get_json()
        post_object = Post(user_login_data)
        post_object.user_id = current_user.id
        db.session.add(post_object)
        db.session.commit()
    return {"message": "Success", "data": user_login_data}


@main.route('/show_all_post/<int:user_id>')
@jwt_required()
def user_post(user_id):
    """Here we get/show the all Post of user by user_id."""
    user_posts = Post.query.filter(Post.user_id == user_id).order_by(
        Post.created_date.desc()).all()

    return jsonify(user_posts)


@main.route('/update_post/<int:post_id>', methods=['POST'])
@jwt_required()
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
@jwt_required()
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
