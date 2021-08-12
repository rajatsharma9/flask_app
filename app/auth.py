from flask import Blueprint, render_template, redirect, url_for, request, flash,session, jsonify # noqa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db
from flask_restful import Resource, Api
from .schema import users_models_schema, SigninFields, LoginSchema

auth = Blueprint('auth', __name__)
api = Api(auth)
user_signin_schema = SigninFields()
user_login_schema = LoginSchema()


class GetAllUsers(Resource):
    """Here we create API to get all users."""

    def get(self, **kwargs):
        """."""
        user_object = User.query.all()
        json_user_object = users_models_schema.dump(user_object)
        return jsonify(json_user_object)

api.add_resource(GetAllUsers, '/get_users')


class Signin(Resource):
    """Here we create API to perform user registration process."""

    def post(self):
        """."""
        user_data = request.get_json()
        errors = user_signin_schema.validate(user_data)
        if errors:
            return errors
        # user = User.query.filter_by(email=user_data.get('email')).first()
        new_user_object = User(fullName=user_data.get('fullName'), email=user_data.get('email'), username=user_data.get('username'), password=generate_password_hash(user_data.get('password')))
        db.session.add(new_user_object)
        db.session.commit()
        return 'Signin Successfully'
api.add_resource(Signin, '/user_signin')


class Login(Resource):
    """Here we create API to perform user login process."""

    def post(self):
        """."""
        user_login_data = request.get_json()
        fields_error_dict = user_login_schema.validate(user_login_data)
        if fields_error_dict:
            return fields_error_dict

        user = User.query.filter_by(email=user_login_data.get('email')).first()

        if check_password_hash(user.password, user_login_data.get('password')):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            session["user"] = True
            login_user(user)
            # flash('Login Successfully')
            return 'Login Successfully'
        return 'Invalid email/password combination'
api.add_resource(Login, '/user_login')


class Logout(Resource):
    """Logout the current user."""

    def get(self):
        """."""
        session['user'] = None
        logout_user()
        return "Logout Successfully"

api.add_resource(Logout, '/user_logout')
