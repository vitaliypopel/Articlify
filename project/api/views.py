from flask import Blueprint, request, jsonify, make_response, flash, redirect, url_for
from project import app, db, current_user, validate_email, os, match, sub
from project.auth import User

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/change-theme', methods=['PATCH'])
def change_theme():
    response = make_response(jsonify())
    req = request.get_json()

    if req:
        theme = req['theme']
        response.set_cookie('theme', theme)
    else:
        return response, 400

    return response, 200


@api.route('/change-username', methods=['PATCH'])
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


@api.route('/change-email', methods=['PATCH'])
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


@api.route('/change-profile-picture', methods=['PATCH'])
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
        old_path = os.path.join(app.root_path, *profile_pictures_path.split('/'), current_user.profile_picture_name)
        if os.path.exists(old_path) and current_user.profile_picture_name != 'default_pfp.svg':
            os.remove(old_path)

        path = os.path.join(app.root_path, *profile_pictures_path.split('/'), filename)
        new_profile_picture.save(path)

        current_user.profile_picture_path = f'images/user_pictures/{filename}'
        current_user.profile_picture_name = filename
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось оновити фото профілю! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Фото профілю успішно змінено', 'success')

    return response, 200


@api.route('/delete-profile-picture', methods=['DELETE'])
def delete_profile_picture():
    response = make_response(jsonify({
        'redirect': url_for('views.account_settings')
    }))

    try:
        old_path = os.path.join(app.root_path, 'static', *current_user.profile_picture_path.split('/'))
        if os.path.exists(old_path):
            os.remove(old_path)

        current_user.profile_picture_path = 'images/user_pictures/default_pfp.svg'
        current_user.profile_picture_name = 'default_pfp.svg'

        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Не вдалось видалити фото профілю! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Фото профілю успішно видалено', 'success')

    return response, 200


@api.route('/change-bio', methods=['PATCH'])
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
