from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap5
from config import Config
from bleach import clean
from datetime import datetime, timedelta
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp
from email_validator import validate_email
from sqlalchemy.sql.expression import func
from secrets import token_urlsafe
from hashlib import sha256
from re import match, sub
import os


app = Flask(__name__)
db = SQLAlchemy()
mongo_db = MongoEngine()
login_manager = LoginManager()
mail = Mail()
bootstrap = Bootstrap5()
config = Config()


def create_app():

    # app.config['MONGODB_SETTINGS'] = config.get('MONGODB_SETTINGS')

    app.config['SECRET_KEY'] = config.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['MONGO_URI'] = config.get('MONGO_URI')
    app.config['TEMPLATES_FOLDER'] = config.get('TEMPLATES_FOLDER')
    app.config['STATIC_FOLDER'] = config.get('STATIC_FOLDER')
    app.config['MAIL_SERVER'] = config.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = config.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = config.get('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = config.get('MAIL_USE_SSL')
    app.config['MAIL_DEFAULT_SENDER'] = config.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_USERNAME'] = config.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config.get('MAIL_PASSWORD')

    from .auth import auth
    app.register_blueprint(auth)

    from .main import views
    app.register_blueprint(views)

    from .api import api
    app.register_blueprint(api)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        from project.main import before_first_request
        before_first_request()

    mongo_db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.log_in'
    login_manager.login_message = 'Будь ласка увійдіть, щоб отримати доступ до цієї сторінки'
    login_manager.login_message_category = 'warning'

    mail.init_app(app)

    bootstrap.init_app(app)

    from project.auth import User

    def user_loader(user_id: int) -> object:
        return User.query.get(user_id)

    app.jinja_env.filters['user_loader'] = user_loader

    from project.main import Article

    def article_loader(article_id: int) -> object:
        return Article.query.get(article_id)

    app.jinja_env.filters['article_loader'] = article_loader

    from project.main import Topic

    def topic_loader(topic_id: int) -> object:
        return Topic.query.get(topic_id)

    app.jinja_env.filters['topic_loader'] = topic_loader

    def datetime_calculation(datetime_before: datetime) -> str:
        delta = datetime.utcnow() - datetime_before
        view_of_time = '{} дн. {:02} год. {:02} хв.'
        time_result = view_of_time.format(delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60)
        return time_result

    app.jinja_env.filters['datetime_calculation'] = datetime_calculation

    def html_clean(text: str) -> str:
        allowed_tags = {'b', 'i', 'a'}
        return clean(text, tags=allowed_tags, strip=False)

    app.jinja_env.filters['html_clean'] = html_clean

    return app
