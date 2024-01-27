from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory, make_response, jsonify
from project.auth import User
from project import db, current_user, login_required, ValidationError, sha256, datetime, os, app
from .models import (
    Feedback,
    Topic, TopicSubscription,
    UserSubscription, UserSubscriptionRequest,
    Article, ArticleTopic, ArticleDocument,
    ArticleView, ArticleLike, ArticleComment,
    SavedArticle
)
from .forms import FeedbackForm
from json import loads

views = Blueprint('views', __name__)


def before_first_request():
    topics = [
        'Python', 'NodeJS', 'C',
        'C++', 'Rust', 'Java',
        'C#', 'Ruby', 'Go',
        'HTML', 'CSS', 'JavaScript',
        'TypeScript', 'PHP', 'SQL',
        'Swift', 'Kotlin', 'Flutter',
        'GIT', 'Linux', 'Networking',
        'Security', 'Clouds', 'DevOps',
        'QA', 'Other'
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


def secret_link(user_id: int, article_id: int) -> str:
    link = f'{user_id}_{article_id}'
    return sha256(link.encode()).hexdigest()


@views.route('/favicon.ico')
def favicon():
    return send_from_directory('static', path='images/icon/icon.jpg')


@views.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.articles'))

    return render_template('main/home.html')


@views.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    response = redirect(url_for('views.feedback'))

    if current_user.is_authenticated and current_user.email_status:
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

    articles_with_topic = ArticleTopic.query.filter_by(topic_id=topic.id).all()

    subscriptions = TopicSubscription.query.filter_by(topic_id=topic.id).all()

    topic_articles = ArticleTopic.query.order_by(ArticleTopic.article_id.desc()).filter_by(topic_id=topic.id).all()
    articles_data = []

    for topic_article in topic_articles:
        article_data = Article.query.filter_by(id=topic_article.article_id, public=True).first()
        if article_data:
            articles_data.append(article_data)

    if current_user.is_authenticated:
        subscription = TopicSubscription.query.filter_by(user_id=current_user.id, topic_id=topic.id).first()
        return render_template('main/topic.html',
                               topic=topic, subscription=subscription, subscriptions=subscriptions,
                               articles_with_topic=articles_with_topic, articles=articles_data)

    return render_template('main/topic.html',
                           topic=topic, subscriptions=subscriptions,
                           articles_with_topic=articles_with_topic, articles=articles_data)


@views.route('/articles')
@login_required
def articles():
    topics_subscriptions = TopicSubscription.query.filter_by(user_id=current_user.id).all()

    articles_data = Article.query.order_by(Article.id.desc()).filter_by(public=True).all()

    return render_template('main/articles.html', title='Рекомендації',
                           topics_subscriptions=topics_subscriptions, articles=articles_data)


@views.route('/followings')
@login_required
def followings():
    topics_subscriptions = TopicSubscription.query.filter_by(user_id=current_user.id).all()

    user_subscriptions = UserSubscription.query.order_by(UserSubscription.id.desc()).filter_by(
                                                                                        user_id=current_user.id).all()
    articles_data = []

    for user_subscription in user_subscriptions:
        user_subscription_articles = Article.query.order_by(Article.id.desc()).filter_by(
                                                                            user_id=user_subscription.author_id,
                                                                            public=True).all()
        articles_data.extend(user_subscription_articles)

    return render_template('main/articles.html', title='Підписки',
                           topics_subscriptions=topics_subscriptions, articles=articles_data)


@views.route('/followings/topics/<topic>')
@login_required
def topics_followings(topic: str):
    topics_subscriptions = TopicSubscription.query.filter_by(user_id=current_user.id).all()

    topic = Topic.query.filter(Topic.topic.ilike(topic)).first()
    if not topic:
        flash('Категорії статей не знайдено', 'danger')
        return redirect(url_for('views.articles_topics'))

    topic_articles = ArticleTopic.query.order_by(ArticleTopic.article_id.desc()).filter_by(topic_id=topic.id).all()
    articles_data = []

    for topic_article in topic_articles:
        article_data = Article.query.filter_by(id=topic_article.article_id, public=True).first()
        if article_data:
            articles_data.append(article_data)

    return render_template('main/articles.html', title=topic.topic,
                           topics_subscriptions=topics_subscriptions, articles=articles_data)


@views.route('/articles/saved')
@login_required
def saved_articles():
    saved_articles_objects = SavedArticle.query.order_by(SavedArticle.id.desc()).filter_by(
                                                                                        user_id=current_user.id).all()

    return render_template('main/saved_articles.html', saved_articles=saved_articles_objects)


@views.route('/articles/builder', methods=['GET', 'POST'])
@login_required
def articles_builder():
    topics = Topic.query.all()

    article_exist = False
    if Article.query.filter_by(user_id=current_user.id).first():
        article_exist = True

    response = make_response(render_template('main/articles_builder.html', topics=topics, article_exist=article_exist))

    if request.method == 'POST':
        files = request.files
        data_json = files['json'].read()
        data = loads(data_json)

        photos = {}
        for data_type, file in files.items():
            if data_type != 'json':
                photos[data_type] = file

        article_document = data['article']
        topics = data['topics']

        last_article = Article.query.order_by(Article.id.desc()).first()
        new_article_id = 1
        if last_article:
            new_article_id = last_article.id + 1

        link = secret_link(current_user.id, new_article_id)

        try:
            article_photos_path = os.path.join(
                app.root_path,
                *url_for('static', filename='images/article_pictures').split('/'),
                link
            )
            os.makedirs(article_photos_path, exist_ok=True)

            for name, photo in photos.items():
                photo_path = os.path.join(article_photos_path, name)

                new_photo = photo
                new_photo.filename = name
                new_photo.save(photo_path)
        except Exception:
            return jsonify(
                {'bad': 'Під час збереження фотографій щось пішло не так! Спробуйте ще раз'}
            )

        title = article_document['title']
        public = article_document['public']
        created_at = datetime.utcnow()

        try:
            new_article = Article(link, title, public, created_at, current_user.id)
            db.session.add(new_article)

            for topic in topics:
                new_topic = ArticleTopic(new_article_id, int(topic))
                db.session.add(new_topic)

            new_article_document = ArticleDocument(link, current_user.id, article_document, str(created_at))
            new_article_document.save()

            db.session.commit()
        except Exception:
            db.session.rollback()

            _article_document = ArticleDocument.objects(link=link).first()
            if _article_document:
                _article_document.delete()

            return jsonify(
                {'bad': 'Щось пішло не так! Спробуйте ще раз'}
            )

        flash('Стаття успішно опублікована', 'success')

        return jsonify(
            {'redirect': url_for('views.article', username=current_user.username, article_link=link)}
        )

    return response


@views.route('/articles/editor/<article_link>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def articles_editor(article_link: str):
    topics = Topic.query.all()

    article_data = Article.query.filter_by(link=article_link.lower(), user_id=current_user.id).first()
    if not article_data:
        flash('Статтю не знайдено', 'warning')
        return redirect(url_for('views.home'))

    _article_document = ArticleDocument.objects(link=article_link.lower(), user_id=current_user.id).first()
    if not _article_document:
        flash('Документ статті не знайдено', 'danger')
        return redirect(url_for('views.home'))

    article_topics_id = []
    for article_topic in ArticleTopic.query.filter_by(article_id=article_data.id).all():
        article_topics_id.append(article_topic.topic_id)

    response = make_response(render_template('main/articles_editor.html',
                                             topics=topics, article_topics_id=article_topics_id,
                                             article=article_data, article_document=_article_document))

    if request.method == 'PUT':
        files = request.files
        data_json = files['json'].read()
        data = loads(data_json)

        existing_photos_json = files['existing_photos'].read()
        existing_photos = loads(existing_photos_json)

        photos = {}
        for data_type, file in files.items():
            if data_type != 'json' and data_type != 'existing_photos':
                photos[data_type] = file

        article_document = data['article']
        topics = data['topics']

        link = article_data.link

        try:
            article_photos_path = os.path.join(
                app.root_path,
                *url_for('static', filename='images/article_pictures').split('/'),
                link
            )
            os.makedirs(article_photos_path, exist_ok=True)

            old_photo_names = [existing_photo['old_photo_name'] for existing_photo in existing_photos]
            for photo in _article_document['article']['photos']:
                print(photo)
                if photo['photo_name'] not in old_photo_names:
                    photo_path = os.path.join(article_photos_path, photo['photo_name'])
                    os.remove(photo_path)

            for existing_photo in existing_photos:
                old_photo_path = os.path.join(article_photos_path, existing_photo['old_photo_name'])
                interactive_photo_path = os.path.join(article_photos_path, existing_photo['interactive_photo_name'])
                if os.path.isfile(old_photo_path):
                    os.rename(old_photo_path, interactive_photo_path)

            for existing_photo in existing_photos:
                interactive_photo_path = os.path.join(article_photos_path, existing_photo['interactive_photo_name'])
                new_photo_path = os.path.join(article_photos_path, existing_photo['new_photo_name'])
                if os.path.isfile(interactive_photo_path):
                    os.rename(interactive_photo_path, new_photo_path)

            for name, photo in photos.items():
                photo_path = os.path.join(article_photos_path, name)

                new_photo = photo
                new_photo.filename = name
                new_photo.save(photo_path)
        except Exception:
            return jsonify(
                {'bad': 'Під час збереження фотографій щось пішло не так! Спробуйте ще раз'}
            )

        title = article_document['title']
        public = article_document['public']
        updated_at = datetime.utcnow()

        old_article_document = _article_document.article
        old_updated_at = _article_document.updated_at if _article_document.updated_at else None

        try:
            article_data.title = title
            article_data.public = public
            article_data.updated_at = updated_at

            for topic in ArticleTopic.query.filter_by(article_id=article_data.id).all():
                db.session.delete(topic)

            for topic in topics:
                new_topic = ArticleTopic(article_data.id, int(topic))
                db.session.add(new_topic)

            _article_document.article = article_document
            _article_document.updated_at = str(updated_at)
            _article_document.save()

            db.session.commit()
        except Exception:
            db.session.rollback()

            article_document = ArticleDocument.objects(link=link).first()
            article_document.article = old_article_document
            article_document.updated_at = old_updated_at
            article_document.save()

            return jsonify(
                {'bad': 'Щось пішло не так! Спробуйте ще раз'}
            )

        flash('Стаття успішно оновлена', 'success')

        return jsonify(
            {'redirect': url_for('views.article', username=current_user.username, article_link=link)}
        )

    if request.method == 'DELETE':
        article_data = Article.query.filter_by(link=article_link.lower(), user_id=current_user.id).first()
        if not article_data:
            flash('Статтю не знайдено', 'warning')
            return jsonify({'redirect': url_for('views.home')})

        article_document = ArticleDocument.objects(link=article_link.lower(), user_id=current_user.id).first()
        saved_articles_ = SavedArticle.query.filter_by(article_id=article_data.id).all()
        article_topics = ArticleTopic.query.filter_by(article_id=article_data.id).all()
        article_views = ArticleView.query.filter_by(article_id=article_data.id).all()
        article_likes = ArticleLike.query.filter_by(article_id=article_data.id).all()
        article_comments = ArticleComment.query.filter_by(article_id=article_data.id).all()

        article_photos_path = os.path.join(
            app.root_path,
            *url_for('static', filename='images/article_pictures').split('/'),
            article_data.link
        )

        try:
            for photo in article_document['article']['photos']:
                photo_path = os.path.join(article_photos_path, photo['photo_name'])
                os.remove(photo_path)
        except Exception as err:
            print(f'Фото не видалились.\n{err}')

        try:
            for saved_article in saved_articles_:
                db.session.delete(saved_article)

            for article_topic in article_topics:
                db.session.delete(article_topic)

            for article_view in article_views:
                db.session.delete(article_view)

            for article_like in article_likes:
                db.session.delete(article_like)

            for article_comment in article_comments:
                db.session.delete(article_comment)

            db.session.delete(article_data)
            db.session.commit()

            article_document.delete()
        except Exception:
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return jsonify(
                {'redirect': url_for('views.article', username=current_user.username, article_link=article_data.link)}
            )

        flash('Стаття успішно видалена', 'success')
        return jsonify({'redirect': url_for('views.home')})

    return response


@views.route('/@<username>')
def profile(username: str):
    user = User.query.filter_by(username=username.lower()).first()

    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    followers = UserSubscription.query.filter_by(author_id=user.id).all()
    followings = UserSubscription.query.filter_by(user_id=user.id).all()

    user_articles = Article.query.filter(Article.public).filter_by(user_id=user.id).order_by(Article.id.desc()).all()

    if current_user.is_authenticated:
        if current_user.id != user.id:
            subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=user.id).first()
            subscription_request = UserSubscriptionRequest.query.filter_by(user_id=current_user.id,
                                                                           author_id=user.id).first()
            return render_template(
                'main/profile.html', user=user,
                subscription=subscription, subscription_request=subscription_request,
                followers=followers, followings=followings, articles=user_articles
            )
        else:
            user_articles = Article.query.filter_by(user_id=current_user.id).order_by(Article.id.desc()).all()
            follow_requests = UserSubscriptionRequest.query.filter_by(author_id=current_user.id).all()
            return render_template(
                'main/profile.html', user=current_user,
                followers=followers, followings=followings,
                follow_requests=follow_requests, articles=user_articles
            )

    return render_template('main/profile.html',
                           user=user, followers=followers, followings=followings, articles=user_articles)


@views.route('/@<username>/about')
def profile_about(username: str):
    user = User.query.filter_by(username=username.lower()).first()

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


@views.route('/@<username>/articles/<article_link>')
def article(username: str, article_link: str):
    bad_response = make_response(redirect(url_for('views.home')))

    user = User.query.filter_by(username=username.lower()).first()
    if not user:
        flash('Користувача не знайдено', 'warning')
        return bad_response

    subscription = None

    if current_user.is_authenticated and current_user.id != user.id:
        subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=user.id).first()

        if not subscription and not user.profile_status:
            flash('Профіль власника закритий! Щоб отримати доступ потрібно підписатись', 'warning')
            return redirect(url_for('views.profile', username=user.username))
    elif not current_user.is_authenticated and not user.profile_status:
        flash('Профіль власника закритий! Щоб отримати доступ потрібно авторизуватись та підписатись', 'warning')
        return redirect(url_for('views.profile', username=user.username))

    article_data = Article.query.filter_by(link=article_link.lower(), user_id=user.id).first()
    if not article_data:
        flash('Статтю не знайдено', 'warning')
        return bad_response

    article_document = ArticleDocument.objects(link=article_link.lower(), user_id=user.id).first()
    if not article_document:
        flash('Документ статті не знайдено', 'danger')
        return bad_response

    if current_user.is_authenticated and current_user.id != user.id and not article_data.public:
        flash('Ця стаття приватна', 'danger')
        return bad_response
    elif not current_user.is_authenticated and not article_data.public:
        flash('Ця стаття приватна', 'danger')
        return bad_response

    try:
        user_id = 0
        if current_user.is_authenticated:
            user_id = current_user.id

        new_view = ArticleView(article_data.id, user_id)
        db.session.add(new_view)
        db.session.commit()
    except Exception:
        flash('Щось пішло не так! Спробуйте ще раз', 'danger')
        return bad_response

    article_views = ArticleView.query.order_by(ArticleView.id.desc()).filter_by(article_id=article_data.id).all()
    article_likes = ArticleLike.query.order_by(ArticleLike.id.desc()).filter_by(article_id=article_data.id).all()
    article_comments = ArticleComment.query.order_by(ArticleComment.id.desc()).filter_by(
                                                                                article_id=article_data.id).all()
    article_topics = ArticleTopic.query.filter_by(article_id=article_data.id).all()

    user_like = None
    user_save = None
    if current_user.is_authenticated:
        user_like = ArticleLike.query.filter_by(article_id=article_data.id, user_id=current_user.id).first()
        user_save = SavedArticle.query.filter_by(article_id=article_data.id, user_id=current_user.id).first()

    return render_template(
        'main/article.html',
        user=user,
        subscription=subscription,
        user_like=user_like,
        user_save=user_save,
        article=article_data,
        article_document=article_document.article,
        views=article_views,
        likes=article_likes,
        comments=article_comments,
        topics=article_topics
    )


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
