from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from project.auth import User
from project import db, current_user, login_required, ValidationError, datetime
from .models import Feedback, Topic
from .forms import FeedbackForm

views = Blueprint('views', __name__)


@views.route('/favicon.ico')
def favicon():

    return send_from_directory('static', path='images/icon/icon.jpg')


@views.route('/')
def home():
    return render_template('main/home.html')


# != prod | admin
@views.route('/topics-auto-complete')
def topics_auto_complete():
    response = dict()

    topics = [
        'Python', 'NodeJS', 'C',
        'C++', 'Rust', 'Java',
        'C#', 'Ruby', 'Go',
        'HTML', 'CSS', 'JavaScript',
        'TypeScript', 'SQL', 'Swift',
        'Kotlin', 'Flutter', 'GIT',
        'Linux', 'Networking', 'Security',
        'Clouds', 'DevOps', 'QA', 'Other'
    ]

    try:
        for topic in topics:
            if not Topic.query.filter_by(topic=topic).first():
                new_topic = Topic(topic)
                db.session.add(new_topic)

                response[topics.index(topic) + 1] = topic

        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify(response)


@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    response = redirect(url_for('views.feedback'))

    if current_user.is_authenticated:
        form.sender_email.data = current_user.email

    if form.validate_on_submit():
        data = form.data
        sender_email = data['sender_email']
        category = data['category']
        body = data['body']

        try:
            form.validate_mail(sender_email)
        except ValidationError as error:
            flash(str(error), 'danger')
            return response

        try:
            new_feedback = Feedback(sender_email, category, body)
            print(new_feedback)
            db.session.add(new_feedback)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return response

        flash('Фідбек успішно відправлено', 'success')

        return response

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return response

    return render_template('main/feedback.html', form=form)


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

