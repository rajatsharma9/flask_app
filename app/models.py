from flask_login import UserMixin  # noqa
import datetime
from . import db


class User(db.Model, UserMixin):
    """Models for User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(120))
    data_created = db.Column(db.DateTime, default=datetime.datetime.now())
    user_posts = db.relationship(
        "Post",
        backref='user',
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        """Function to represent Data in Terminal."""
        return f"<User(user_id:{self.id}, user_name:{self.fullName})>" # noqa


class Post(db.Model):
    """Models for user Post."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(30), nullable=False)
    post_subtitle = db.Column(db.String(80), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_by = db.relationship("User", backref="post")

    def __init__(self, data):
        """Here we create constructor of this class."""
        self.post_title = data.get('post_title')
        self.post_subtitle = data.get('post_subtitle')
        self.post_content = data.get('post_content')

    def __repr__(self):
        """Function to represent Data in Terminal."""
        return f"<Post(post_id:{self.id}, title:{self.post_title})>"
