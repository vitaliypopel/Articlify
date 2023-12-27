from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap5
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp
from email_validator import validate_email
from datetime import datetime, timedelta
from secrets import token_urlsafe


app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bootstrap = Bootstrap5()


def create_app():

    app.config['SECRET_KEY'] = 'this_is_my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['TEMPLATES_FOLDER'] = 'project/templates'
    app.config['STATIC_FOLDER'] = 'project/static'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'popelcompany@gmail.com'
    app.config['MAIL_USERNAME'] = 'popelcompany@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xvcexfmxbgwcwhnz'

    from .auth import auth
    app.register_blueprint(auth)

    from .main import views
    app.register_blueprint(views)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'auth.log_in'
    login_manager.login_message = 'Будь ласка увійдіть, щоб отримати доступ до цієї сторінки'
    login_manager.login_message_category = 'warning'

    mail.init_app(app)

    bootstrap.init_app(app)

    return app
