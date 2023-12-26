from flask import Blueprint, render_template, request, flash, redirect, url_for
from project.auth import User

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('main/home.html')


@views.route('/<username>')
@views.route('/@<username>')
def profile(username: str):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    return render_template('main/profile.html', user=user)


@views.route('/favicon.ico')
def favicon():
    return 'icon'
