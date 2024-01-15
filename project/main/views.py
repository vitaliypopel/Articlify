from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response, jsonify
from project.auth import User
from project import db, current_user, login_required, ValidationError, datetime
from .models import Feedback, Topic, TopicSubscription, UserSubscription, UserSubscriptionRequest
from .forms import FeedbackForm

views = Blueprint('views', __name__)


def before_first_request():
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
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise Exception('Щось пішло не так!!!')


@views.route('/favicon.ico')
def favicon():

    return send_from_directory('static', path='images/icon/icon.jpg')


@views.route('/')
def home():

    if current_user.is_authenticated:
        topic_subscriptions = TopicSubscription.query.filter_by(user_id=current_user.id).all()
        return render_template('main/home.html', topic_subscriptions=topic_subscriptions)

    return render_template('main/home.html')


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


# != production by the moment
@views.route('/articles')
def articles():
    ...


@views.route('/articles/topics')
def articles_topics():
    topics = Topic.query.all()
    response = make_response(render_template('main/topics.html', topics=topics))

    return response


@views.route('/articles/topics/<topic>')
def articles_topic(topic: str):
    topic = Topic.query.filter(Topic.topic.ilike(topic)).first()

    if not topic:
        flash('Категорії статей не знайдено', 'danger')
        return redirect(url_for('views.articles_topics'))

    subscriptions = TopicSubscription.query.filter_by(topic_id=topic.id).all()

    if current_user.is_authenticated:
        subscription = TopicSubscription.query.filter_by(user_id=current_user.id, topic_id=topic.id).first()
        return render_template('main/topic.html', topic=topic, subscription=subscription, subscriptions=subscriptions)

    return render_template('main/topic.html', topic=topic, subscriptions=subscriptions)


@views.route('/@<username>')
def profile(username: str):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    followers = UserSubscription.query.filter_by(author_id=user.id).all()
    followings = UserSubscription.query.filter_by(user_id=user.id).all()

    if current_user.is_authenticated:
        if current_user.id != user.id:
            subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=user.id).first()
            subscription_request = UserSubscriptionRequest.query.filter_by(user_id=current_user.id,
                                                                           author_id=user.id).first()
            return render_template(
                'main/profile.html', user=user,
                subscription=subscription, subscription_request=subscription_request,
                followers=followers, followings=followings
            )
        else:
            follow_requests = UserSubscriptionRequest.query.filter_by(author_id=current_user.id).all()
            return render_template(
                'main/profile.html', user=current_user,
                followers=followers, followings=followings,
                follow_requests=follow_requests
            )

    return render_template('main/profile.html', user=user, followers=followers, followings=followings)


@views.route('/@<username>/about')
def profile_about(username: str):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    followers = UserSubscription.query.filter_by(author_id=user.id).all()
    followings = UserSubscription.query.filter_by(user_id=user.id).all()

    if current_user.is_authenticated:
        if current_user.id != user.id:
            subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=user.id).first()
            subscription_request = UserSubscriptionRequest.query.filter_by(user_id=current_user.id,
                                                                           author_id=user.id).first()
            return render_template(
                'main/profile_about.html', user=user,
                subscription=subscription, subscription_request=subscription_request,
                followers=followers, followings=followings
            )
        else:
            follow_requests = UserSubscriptionRequest.query.filter_by(author_id=current_user.id).all()
            return render_template(
                'main/profile_about.html', user=current_user,
                followers=followers, followings=followings,
                follow_requests=follow_requests
            )

    return render_template('main/profile_about.html', user=user, followers=followers, followings=followings)


@views.route('/settings')
@views.route('/settings/general')
@login_required
def settings():
    return render_template('main/settings.html')


@views.route('/settings/account')
@login_required
def account_settings():
    return render_template('main/account_settings.html')


@views.route('/settings/security')
@login_required
def security_settings():
    return render_template('main/security_settings.html')


@views.route('/articles/builder', methods=['GET', 'POST'])
@login_required
def articles_builder():
    topics = Topic.query.all()
    response = make_response(render_template('main/articles_builder.html', topics=topics))

    if request.method == 'POST':
        data = request.get_json()
        article = {
            'id': 1,
            'link': 'secret_link_lol',
            'article': data['article'],
            'created_at': str(datetime.utcnow()),
            'updated_at': None
        }

        with open('article_test.json', 'w', encoding='utf-8') as file:
            from json import dumps
            article_test = dumps(article, indent=4, ensure_ascii=False)
            file.write(article_test)

        return jsonify({})

    return response
