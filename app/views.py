from . import db, ALLOWED_EXTENSIONS # noqa
from .models import Post, User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
import uuid

main = Blueprint('main', __name__)


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


def allowed_file(filename):
    """Return File with defined extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    """Show User profile and uplode image."""
    image_url = url_for('static', filename='user_profile_img/' + current_user.image_file)
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' or 'file' not in request.files:
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            key = uuid.uuid1()
            img = request.files["file"]
            img_new_name = f"{key}{img.filename}" # noqa
            path = os.path.join(main.root_path, 'static/user_profile_img', img_new_name)
            img.save(path)
            current_user.image_file = img_new_name
            db.session.commit()
        image_url = url_for('static', filename='user_profile_img/' + current_user.image_file)
    return render_template('userProfile.html', image_url=image_url, user=current_user)
