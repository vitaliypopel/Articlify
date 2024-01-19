from flask import Blueprint, request, jsonify, make_response, flash, redirect, url_for
from project import app, db, current_user, login_required, validate_email, os, match, sub
from project.auth import User
from project.main import Topic, TopicSubscription, UserSubscription, UserSubscriptionRequest

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/change/theme', methods=['PATCH'])
def change_theme():
    response = make_response(jsonify())
    req = request.get_json()

    if req:
        theme = req['theme']
        response.set_cookie('theme', theme)
    else:
        return response, 400

    return response, 200


@api.route('/change/username', methods=['PATCH'])
@login_required
def change_username():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    req = request.get_json()
    new_username = req['new_username'].lower()

    if len(new_username) < 2 or len(new_username) > 20:
        flash('Ім\'я повинне містити від 2 до 20 символів', 'danger')
        return response, 400

    if not match(r'^[a-zA-Z0-9_]*$', new_username):
        flash('Ім\'я повинне використовувати тільки латиницю, цифри та підкреслення', 'danger')
        return response, 400

    if current_user.username == new_username:
        return response, 400

    if User.query.filter_by(username=new_username).first():
        flash('Ім\'я вже зайняте! Спробуйте використати інше', 'danger')
        return response, 400

    try:
        current_user.username = new_username
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось змінити ім\'я! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Ім\'я успішно змінене', 'success')
    return response, 200


@api.route('/change/email', methods=['PATCH'])
@login_required
def change_email():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    req = request.get_json()
    new_email = req['new_email']

    if len(new_email) < 4 or len(new_email) > 100:
        flash('Електронна пошта повинна містити від 4 до 100 символів', 'danger')
        return response, 400

    if current_user.email == new_email:
        return response, 400

    if User.query.filter_by(email=new_email).first():
        flash('Електронна пошта вже зайнята! Спробуйте використати іншу', 'danger')
        return response, 400

    try:
        validate_email(new_email)
    except Exception:
        flash('Неправильна електронна пошта! Спробуйте ще раз', 'danger')
        return response, 400

    try:
        current_user.email = new_email
        current_user.email_status = False
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось змінити електронну пошту! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Електронну пошту успішно змінено', 'success')
    return response, 200


@api.route('/change/profile-picture', methods=['PATCH'])
@login_required
def change_profile_picture():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    profile_pictures_path = url_for('static', filename='images/user_pictures')

    req = request.files
    new_profile_picture = req['new_profile_picture']

    filename = f'user_{current_user.id}_pfp.{new_profile_picture.content_type.replace("image/", "")}'
    new_profile_picture.filename = filename

    try:
        old_path = os.path.join(app.root_path, *profile_pictures_path.split('/'), current_user.profile_picture)
        if os.path.exists(old_path) and current_user.profile_picture != 'default_pfp.png':
            os.remove(old_path)

        path = os.path.join(app.root_path, *profile_pictures_path.split('/'), filename)
        new_profile_picture.save(path)

        current_user.profile_picture = filename
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось оновити фото профілю! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Фото профілю успішно змінено', 'success')
    return response, 200


@api.route('/delete/profile-picture', methods=['DELETE'])
@login_required
def delete_profile_picture():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    try:
        old_path = os.path.join(app.root_path, 'static/images/user_pictures', current_user.profile_picture)
        if os.path.exists(old_path):
            os.remove(old_path)

        current_user.profile_picture = 'default_pfp.png'
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось видалити фото профілю! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Фото профілю успішно видалено', 'success')
    return response, 200


@api.route('/change/bio', methods=['PATCH'])
@login_required
def change_bio():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    req = request.get_json()

    new_bio = req['new_bio']
    new_bio = [sub(r'\s+', ' ', line).strip() for line in new_bio.split('\n')]
    new_bio = '\n'.join(new_bio)

    try:
        current_user.bio = new_bio
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось змінити біографію! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Біографію успішно змінено', 'success')
    return response, 200


@api.route('/change/profile-status', methods=['PATCH'])
@login_required
def change_profile_status():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    req = request.get_json()

    new_profile_status = req['new_profile_status']

    try:
        current_user.profile_status = new_profile_status

        if current_user.profile_status:
            follow_requests = UserSubscriptionRequest.query.filter_by(author_id=current_user.id).all()

            for follow_request in follow_requests:
                new_subscription = UserSubscription(follow_request.user_id, current_user.id)
                db.session.add(new_subscription)
                db.session.delete(follow_request)

        db.session.commit()
    except Exception as error:
        print(error)
        flash('Не вдалось змінити статус профілю! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Статус профілю успішно змінено', 'success')
    return response, 200


@api.route('/follow/user/<author_id>', methods=['POST'])
@login_required
def follow_user(author_id: int):
    response = make_response(jsonify())

    author = User.query.get(author_id)
    if not author:
        return response, 400

    subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=author.id).first()
    if not subscription:
        try:
            new_subscription = UserSubscription(current_user.id, author.id)
            db.session.add(new_subscription)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200


@api.route('/unfollow/user/<author_id>', methods=['DELETE'])
@login_required
def unfollow_user(author_id: int):
    response = make_response(jsonify())

    author = User.query.get(author_id)
    if not author:
        return response, 400

    subscription = UserSubscription.query.filter_by(user_id=current_user.id, author_id=author.id).first()
    if subscription:
        try:
            db.session.delete(subscription)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200


@api.route('/follow/request/user/<author_id>', methods=['POST'])
@login_required
def follow_request_user(author_id: int):
    response = make_response(jsonify())

    author = User.query.get(author_id)
    if not author:
        return response, 400

    if author.profile_status:
        return response, 400

    subscription_request = UserSubscriptionRequest.query.filter_by(user_id=current_user.id, author_id=author.id).first()
    if not subscription_request:
        try:
            new_subscription_request = UserSubscriptionRequest(current_user.id, author.id)
            db.session.add(new_subscription_request)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200


@api.route('/unfollow/request/user/<author_id>', methods=['DELETE'])
@login_required
def unfollow_request_user(author_id: int):
    response = make_response(jsonify())

    author = User.query.get(author_id)
    if not author:
        return response, 400

    if author.profile_status:
        return response, 400

    subscription_request = UserSubscriptionRequest.query.filter_by(user_id=current_user.id, author_id=author.id).first()
    if subscription_request:
        try:
            db.session.delete(subscription_request)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200


@api.route('/follow/request/user/<author_id>/accept/<user_id>', methods=['POST'])
@login_required
def follow_request_accept(author_id: int, user_id: int):
    response = make_response(jsonify())

    user = User.query.get(user_id)
    if not user:
        return response, 400

    author = User.query.get(author_id)
    if author.id != current_user.id:
        return response, 400

    subscription_request = UserSubscriptionRequest.query.filter_by(user_id=user.id, author_id=current_user.id).first()
    if not subscription_request:
        return response, 400

    try:
        new_subscription = UserSubscription(user.id, current_user.id)
        db.session.add(new_subscription)
        db.session.delete(subscription_request)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return response, 400

    return response, 200


@api.route('/follow/request/user/<author_id>/reject/<user_id>', methods=['DELETE'])
@login_required
def follow_request_reject(author_id: int, user_id: int):
    response = make_response(jsonify())

    user = User.query.get(user_id)
    if not user:
        return response, 400

    author = User.query.get(author_id)
    if author.id != current_user.id:
        return response, 400

    subscription_request = UserSubscriptionRequest.query.filter_by(user_id=user.id, author_id=current_user.id).first()
    if not subscription_request:
        return response, 400

    try:
        db.session.delete(subscription_request)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return response, 400

    return response, 200


@api.route('/follow/user/<author_id>/delete/<user_id>', methods=['DELETE'])
@login_required
def delete_follower(author_id: int, user_id: int):
    response = make_response(jsonify())

    user = User.query.get(user_id)
    if not user:
        return response, 400

    author = User.query.get(author_id)
    if author.id != current_user.id:
        return response, 400

    subscription = UserSubscription.query.filter_by(user_id=user.id, author_id=current_user.id).first()
    if not subscription:
        return response, 400

    try:
        db.session.delete(subscription)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return response, 400

    return response, 200


@api.route('/follow/topic/<topic_id>', methods=['POST'])
@login_required
def follow_topic(topic_id: int):
    response = make_response(jsonify())

    topic = Topic.query.get(topic_id)
    if not topic:
        return response, 400

    subscription = TopicSubscription.query.filter_by(user_id=current_user.id, topic_id=topic.id).first()
    if not subscription:
        try:
            new_subscription = TopicSubscription(current_user.id, topic.id)
            db.session.add(new_subscription)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200


@api.route('/unfollow/topic/<topic_id>', methods=['DELETE'])
@login_required
def unfollow_topic(topic_id: int):
    response = make_response(jsonify())

    topic = Topic.query.get(topic_id)
    if not topic:
        return response, 400

    subscription = TopicSubscription.query.filter_by(user_id=current_user.id, topic_id=topic.id).first()
    if subscription:
        try:
            db.session.delete(subscription)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return response, 400

    return response, 200
