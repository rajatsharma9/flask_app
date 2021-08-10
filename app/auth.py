from flask import Blueprint, render_template, redirect, url_for, request, flash,session, jsonify # noqa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db
from flask_restful import Resource, Api
from .schema import users_models_schema

auth = Blueprint('auth', __name__)
api = Api(auth)


class GetAllUsers(Resource):
    """Here we create API to get all users."""

    def get(self, **kwargs):
        """."""
        user_object = User.query.all()
        print(users_models_schema)
        json_user_object = users_models_schema.dump(user_object)
        return jsonify(json_user_object)

api.add_resource(GetAllUsers, '/get_users/<int:post_id>')


class Signin(Resource):
    """Here we create API to perform user registration process."""

    def post(self):
        """."""
        user_data = request.get_json()
        user = User.query.filter_by(email=user_data.get('email')).first()

        if user:
            flash('A user already exists with that email address.')
            return 'User exists'

        new_user_object = User(fullName=user_data.get('fullname'), email=user_data.get('email'), username=user_data.get('username'), password=generate_password_hash(user_data.get('password')))
        db.session.add(new_user_object)
        db.session.commit()
        return 'registration successful'
api.add_resource(Signin, '/user_signin')


class Login(Resource):
    """Here we create API to perform user login process."""

    def post(self):
        """."""
        user_login_data = request.get_json()

        user = User.query.filter_by(email=user_login_data.get('email')).first()

        if user and check_password_hash(user.password, user_login_data.get('password')):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            session["user"] = True
            login_user(user)
            # flash('Login Successfully')
            return 'Login Successfully'
        return 'Invalid username/password combination'
api.add_resource(Login, '/user_login')


class Logout(Resource):
    """Logout the current user."""

    def get(self):
        """."""
        session['user'] = None
        logout_user()
        return "Logout Successfully"

api.add_resource(Logout, '/user_logout')
