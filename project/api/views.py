from flask import Blueprint, request, jsonify, make_response, flash, redirect, url_for
from project import db, current_user, validate_email, match
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
        flash('Щось пішло не так! Спробуйте ще раз', 'danger')
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
        flash('Емейл вже зайнятий! Спробуйте використати інший', 'danger')
        return response, 400

    try:
        validate_email(new_email)
    except Exception:
        flash('Неправильний емейл! Спробуйте ще раз', 'danger')
        return response, 400

    try:
        current_user.email = new_email
        current_user.email_status = False
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Щось пішло не так! Спробуйте ще раз', 'danger')
        return response, 400

    flash('Емейл успішно змінено', 'success')
    return response, 200


@api.route('/change-profile-picture', methods=['PATCH'])
def change_profile_picture():
    profile_picture_path = url_for('static', filename='images/user_pictures')
    ...
