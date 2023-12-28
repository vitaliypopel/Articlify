from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from project.auth import User
from project import current_user, login_required, mail, Message

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('main/home.html')


@views.route('/@<username>')
def profile(username: str):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    return render_template('main/profile.html', user=user)


@views.route('/@<username>/about')
def profile_about(username: str):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    return render_template('main/profile_about.html', user=user)


# != prod
@views.route('/theme', methods=['GET', 'POST'])
def theme():
    response = make_response(render_template('main/theme.html'))

    if request.method == 'POST':
        _theme = request.form.get('theme')
        response.set_cookie('theme', _theme)
        
    return response


# != prod
@views.route('/favicon.ico')
def favicon():
    return 'icon'
