from flask import Blueprint, make_response, render_template, request, flash, redirect, url_for
from project import db, login_manager, login_required, login_user, logout_user, current_user, ValidationError
from project import generate_password_hash, check_password_hash
from project import mail, Message, datetime
from .models import User, EmailConfirmation, ResetPassword
from .forms import SignUpForm, LogInForm, ChangePasswordForm, ResetPasswordForm, PasswordResettingForm

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id: int | str) -> object:
    return User.query.get(int(user_id))


@auth.route('/signup', methods=['GET', 'POST'])
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    response = make_response(render_template('auth/sign_up.html', form=form))

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if form.validate_on_submit():
        data = form.data
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']

        try:
            form.validate_name(username)
            form.validate_mail(email)
            form.password_confirmation(password, confirm_password)
        except ValidationError as error:
            flash(str(error), 'danger')
            return redirect(url_for('auth.sign_up'))

        try:
            new_user = User(username, generate_password_hash(password), email)
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return redirect(url_for('auth.sign_up'))

        try:
            new_confirmation = EmailConfirmation(new_user.id)
            db.session.add(new_confirmation)
            db.session.commit()

            send_email_confirmation(new_user.email, new_user.id, new_confirmation.token)
        except Exception:
            db.session.rollback()
            return redirect(url_for('auth.sign_up'))

        flash('Реєстрація пройшла успішно! Будь ласка увійдіть', 'success')
        return redirect(url_for('auth.log_in'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return redirect(url_for('auth.sign_up'))

    return response


@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/log-in', methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    response = make_response(render_template('auth/log_in.html', form=form))

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if form.validate_on_submit():
        data = form.data
        username = data['username'].lower()
        password = data['password']

        try:
            form.validate_name(username)
        except ValidationError as error:
            flash(str(error), 'danger')
            return redirect(url_for('auth.log_in'))

        try:
            user = User.query.filter_by(username=username).first()
            if check_password_hash(user.password, password):
                login_user(user)
            else:
                flash('Не правильний пароль! Спробуйте ще раз', 'danger')
                return redirect(url_for('auth.log_in'))
        except Exception:
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return redirect(url_for('auth.log_in'))

        flash(f'Вітаємо, {username}! Вхід успішно виконано', 'success')

        if not current_user.email_status:
            account_settings_url = url_for('views.account_settings')

            flash(
                f'Ваша електронна пошта не підтверджена! Зробити це можна в '
                f'<a class="btn-link" style="text-decoration: none;" href="{account_settings_url}">налаштуваннях</a>',
                'warning'
            )

        return redirect(url_for('views.home'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return redirect(url_for('auth.log_in'))

    return response


@auth.route('/logout')
@auth.route('/log-out')
@login_required
def log_out():
    response = make_response(redirect(url_for('views.home')))

    try:
        logout_user()
    except Exception:
        flash('Щось пішло не так! Спробуйте ще раз')
    else:
        flash('Вихід успішно виконаний', 'success')

    return response


def send_email_confirmation(email: str, user_id: str, token: str) -> None:
    url = url_for(
        "auth.email_confirmation",
        user_id=user_id,
        token=token,
        _external=True
    )

    recipient = email
    subject = 'Articlify'
    template = render_template('newsletter/email_confirmation.html', user_id=user_id, url=url)

    message = Message(recipients=[recipient], subject=subject, html=template)
    mail.send(message)


def send_success_email_confirmation(email: str) -> None:
    recipient = email
    subject = 'Articlify'
    template = render_template('newsletter/email_confirmed.html')

    message = Message(recipients=[recipient], subject=subject, html=template)
    mail.send(message)


def send_reset_password(email: str, user_id: str, token: str) -> None:
    url = url_for(
        "auth.password_resetting",
        user_id=user_id,
        token=token,
        _external=True
    )

    recipient = email
    subject = 'Articlify'
    template = render_template('newsletter/reset_password.html', url=url)

    message = Message(recipients=[recipient], subject=subject, html=template)
    mail.send(message)


def send_success_reset_password(email: str) -> None:
    recipient = email
    subject = 'Articlify'
    template = render_template('newsletter/password_reseted.html')

    message = Message(recipients=[recipient], subject=subject, html=template)
    mail.send(message)


@auth.route('/confirm-email')
@login_required
def confirm_email():
    response = make_response(redirect(url_for('views.account_settings')))

    if current_user.email_status:
        flash('Ви вже підтвердити свою електронну пошту', 'warning')
        return response

    try:
        confirmations = EmailConfirmation.query.filter_by(user_id=current_user.id).all()
        for conf in confirmations:
            db.session.delete(conf)

        new_confirmation = EmailConfirmation(current_user.id)
        db.session.add(new_confirmation)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Щось пішло не так! Спробуйте ще раз', 'warning')
        return response

    try:
        send_email_confirmation(current_user.email, current_user.id, new_confirmation.token)
    except Exception:
        flash('Повідомлення не надіслано! Спробуйте ще раз', 'danger')
        return response
    else:
        flash(f'Повідомлення для підтвердження надіслано на {current_user.email}', 'success')

    return response


@auth.route('/confirm-email/<user_id>/<token>')
def email_confirmation(user_id: str, token: str):
    response = None

    if current_user.is_authenticated:
        if current_user.id == user_id:
            response = make_response(redirect(url_for('views.account_settings')))
        else:
            flash('Ви не можете підтвердити чужу електронну пошту')
            return redirect(url_for('views.home'))
    else:
        response = make_response(redirect(url_for('views.home')))

    confirmation = EmailConfirmation.query.filter_by(token=token, user_id=user_id).first()

    if not confirmation:
        flash('Токен не знайдено', 'warning')
        return response

    user = User.query.get(user_id)
    if not user:
        flash('Користувача не знайдено', 'warning')
        return response

    if user.email_status:
        flash('Ви вже підтвердили свою електронну пошту', 'warning')
        return response

    if confirmation.expiration_time < datetime.utcnow():
        try:
            db.session.delete(confirmation)

            confirmations = EmailConfirmation.query.filter_by(user_id=user.id)
            for conf in confirmations:
                db.session.delete(conf)

            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
        else:
            flash('Час на підтвердження вийшов! Спробуйте надіслати підтвердження повторно', 'danger')

        return response

    try:
        user.email_status = True
        db.session.delete(confirmation)

        confirmations = EmailConfirmation.query.filter_by(user_id=user.id).all()
        for conf in confirmations:
            db.session.delete(conf)

        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Щось пішло не так! Спробуйте ще раз', 'danger')
        return response
    else:
        flash(f'Ви успішно підтвердили електронну пошту {user.email}', 'success')

    try:
        send_success_email_confirmation(user.email)
    except Exception:
        return response

    return response


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    response = make_response(render_template('auth/reset_password.html', form=form))
    bad_response = make_response(redirect(url_for('auth.reset_password')))

    if form.validate_on_submit():
        data = form.data
        username = data['username'].lower()

        try:
            form.validate_name(username)
        except ValidationError as error:
            flash(str(error), 'danger')
            return bad_response

        user = User.query.filter_by(username=username).first()
        if not user.email_status:
            flash('Ваша пошта не підтверджена! Будь ласка підтвердіть вашу пошту', 'warning')
            try:
                confirmations = EmailConfirmation.query.filter_by(user_id=user.id)
                for conf in confirmations:
                    db.session.delete(conf)

                new_confirmation = EmailConfirmation(user.id)
                db.session.add(new_confirmation)
                db.session.commit()

                send_email_confirmation(user.email, user.id, new_confirmation.token)
            except Exception:
                flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            else:
                flash(f'Повідомлення для підтвердження надіслано на {user.email}', 'success')

            return redirect(url_for('views.home'))

        try:
            reset_passwords = ResetPassword.query.filter_by(user_id=user.id).all()
            for reset in reset_passwords:
                db.session.delete(reset)

            new_reset_password = ResetPassword(user.id)
            db.session.add(new_reset_password)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return bad_response

        try:
            send_reset_password(user.email, user.id, new_reset_password.token)
        except Exception:
            flash('Повідомлення не надіслано! Спробуйте ще раз', 'danger')
            return bad_response
        else:
            flash(f'Посилання для скидання паролю надіслано на {user.email}', 'success')

        return redirect(url_for('views.home'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return bad_response

    return response


@auth.route('/reset-password/<user_id>/<token>', methods=['GET', 'POST'])
def password_resetting(user_id: str, token: str):
    form = PasswordResettingForm()
    response = make_response(render_template('auth/password_resetting.html', form=form))
    bad_response = make_response(redirect(url_for('auth.password_resetting', user_id=user_id, token=token)))

    reset = ResetPassword.query.filter_by(user_id=user_id, token=token).first()
    if not reset:
        flash('Токен не знайдено', 'warning')
        return redirect(url_for('views.home'))

    user = User.query.get(user_id)
    if not user:
        flash('Користувача не знайдено', 'warning')
        return redirect(url_for('views.home'))

    if form.validate_on_submit():
        data = form.data

        new_password = data['new_password']
        confirm_new_password = data['confirm_new_password']

        try:
            form.password_confirmation(new_password, confirm_new_password)
        except ValidationError as error:
            flash(str(error), 'danger')
            return bad_response

        try:
            reset_passwords = ResetPassword.query.filter_by(user_id=user.id).all()
            for reset in reset_passwords:
                db.session.delete(reset)

            user.password = generate_password_hash(new_password)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return bad_response
        else:
            flash('Пароль успішно змінено', 'success')

        try:
            send_success_reset_password(user.email)
        except Exception:
            return redirect(url_for('auth.log_in'))

        return redirect(url_for('auth.log_in'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return bad_response

    return response


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    response = make_response(render_template('auth/change_password.html', form=form))
    bad_response = make_response(redirect(url_for('auth.change_password')))

    if form.validate_on_submit():
        data = form.data

        password = data['password']
        new_password = data['new_password']
        confirm_new_password = data['confirm_new_password']

        try:
            form.password_confirmation(new_password, confirm_new_password)
        except ValidationError as error:
            flash(str(error), 'danger')
            return bad_response

        if check_password_hash(current_user.password, generate_password_hash(password)):
            flash('Не правильний пароль! Спробуйте ще раз', 'danger')
            return bad_response

        try:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Щось пішло не так! Спробуйте ще раз', 'danger')
            return bad_response

        flash('Пароль успішно змінено', 'success')
        return redirect(url_for('views.security_settings'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return bad_response

    return response
