from flask import Blueprint, render_template, request, flash, redirect, url_for
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


@views.route('/send-mail')
@login_required
def send_mail():
    recipient = current_user.email
    subject = 'Title'
    body = 'Text'

    try:
        message = Message(recipients=[recipient], subject=subject, body=body)
        mail.send(message)
    except Exception as error:
        print(f'{error}')
    else:
        flash('Повідомлення надіслано', 'success')

    return redirect(url_for('views.home'))


@views.route('/favicon.ico')
def favicon():
    return 'icon'
