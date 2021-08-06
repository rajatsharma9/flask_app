from flask import Flask  # noqa
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
sess = Session()
api = Api()

marshl = Marshmallow()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__)
    bcrypt = Bcrypt(app)   # noqa

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/BluePrintDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)

    api.init_app(app)
    marshl.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
