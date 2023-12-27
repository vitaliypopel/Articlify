from flask import Blueprint, make_response, render_template, request, flash, redirect, url_for
from project import db, login_manager, login_required, login_user, logout_user, current_user, ValidationError
from project import generate_password_hash, check_password_hash
from project import mail, Message, datetime
from .models import User, EmailConfirmation
from .forms import SignUpForm, LogInForm, LogOutForm, EmailConfirmationForm

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
        username = data['username'].lower()
        email = data['email'].lower()
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
        else:
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
        return redirect(url_for('views.home'))

    elif form.errors:
        form_errors = form.errors
        for errors in form_errors.values():
            for error in errors:
                flash(str(error), 'danger')

        return redirect(url_for('auth.log_in'))

    return response


@auth.route('/logout', methods=['GET', 'POST'])
@auth.route('/log-out', methods=['GET', 'POST'])
@login_required
def log_out():
    form = LogOutForm()
    response = make_response(render_template('auth/log_out.html', form=form))

    if form.validate_on_submit():
        data = form.data

        if data['submit']:
            logout_user()
            flash('Вихід успішно виконаний', 'success')

        return redirect(url_for('views.home'))

    return response


@auth.route('/@<username>/confirm-email', methods=['GET', 'POST'])
def confirm_email(username: str):
    form = EmailConfirmationForm()
    user = User.query.filter_by(username=username).first()
    response = make_response(render_template('auth/confirm_email.html', form=form, user=user))
    home_redirect = make_response(redirect(url_for('views.home')))

    if not user:
        flash('Користувача не знайдено', 'warning')
        return home_redirect

    if current_user.id != user.id:
        flash('Ви не можете підтвердити чужу електронну пошту', 'danger')
        return home_redirect

    if current_user.email_status:
        flash('Ви вже підтвердили свою електронну пошту', 'warning')
        return home_redirect

    if form.validate_on_submit():
        data = form.data

        if data['submit']:
            try:
                confirmations = EmailConfirmation.query.filter_by(user_id=current_user.id)
                for conf in confirmations:
                    db.session.delete(conf)

                new_confirmation = EmailConfirmation(current_user.id)
                db.session.add(new_confirmation)
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash('Щось пішло не так! Спробуйте ще раз', 'warning')
                return home_redirect

            url = url_for(
                "auth.email_confirmation",
                username=current_user.username,
                token=new_confirmation.token,
                _external=True
            )

            recipient = current_user.email
            subject = 'Articlify'
            body = f'<h1>Для того, щоб підтвердити пошту перейдіть по посиланню нижче:</h1>\n' \
                   f'<h3><a href="{url}">Посилання для підтвердження пошти</a></h3>'

            try:
                message = Message(recipients=[recipient], subject=subject, html=body)
                mail.send(message)
            except Exception:
                flash('Повідомлення не надіслано! Спробуйте ще раз', 'danger')
                return home_redirect
            else:
                flash(f'Повідомлення для підтвердження наліслано на {current_user.email}', 'success')

        return home_redirect

    return response


@auth.route('/@<username>/confirm-email/<token>')
def email_confirmation(username: str, token: str):
    user = User.query.filter_by(username=username).first()
    confirmation = EmailConfirmation.query.filter_by(token=token).first()
    response = make_response(redirect(url_for('views.home')))

    if not user:
        flash('Користувача не знайдено', 'warning')
        return response

    if not confirmation:
        flash('Токен не знайдено', 'warning')
        return response

    if current_user.id != user.id:
        flash('Ви не можете підтвердити чужу електронну пошту', 'danger')
        return response

    if current_user.email_status:
        flash('Ви вже підтвердили свою електронну пошту', 'warning')
        return response

    if confirmation.expiration_time < datetime.utcnow():
        flash('Час на підтвердження вийшов! Спробуйте надіслати підтвердження повторно', 'danger')
        return response

    try:
        confirmations = EmailConfirmation.query.filter_by(user_id=current_user.id)
        for conf in confirmations:
            db.session.delete(conf)

        current_user.email_status = True
        db.session.delete(confirmation)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Щось пішло не так! Спробуйте ще раз', 'danger')
        return response
    else:
        flash(f'Ви успішно підтвердили електронну пошту {current_user.email}')

    recipient = current_user.email
    subject = 'Articlify'
    body = f'<h1>Підтвердження електронної пошти</h1>\n' \
           f'<h3>Ви успішно підтвердили цю електронну пошту!</h3>'

    try:
        message = Message(recipients=[recipient], subject=subject, html=body)
        mail.send(message)
    except Exception:
        return response

    return response


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    response = make_response(render_template('layout.html'))
    return response
