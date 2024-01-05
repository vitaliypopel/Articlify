from project import (
    FlaskForm,
    StringField,
    PasswordField,
    EmailField,
    SubmitField,
    InputRequired,
    Length,
    Regexp,
    ValidationError,
    validate_email
)
from .models import User


class SignUpForm(FlaskForm):
    username = StringField(
        label='Ім\'я',
        validators=[
            InputRequired(),
            Length(min=2, max=20, message='Ім\'я повинне містити від 2 до 20 символів'),
            Regexp(r'^[a-zA-Z0-9_]*$', message='Ім\'я повинне використовувати тільки латиницю, цифри та підкреслення')
        ]
    )

    email = EmailField(
        label='Електронна пошта',
        validators=[
            InputRequired(),
            Length(min=4, max=100, message='Електронна пошта повинна містити від 4 до 100 символів')
        ]
    )

    password = PasswordField(
        label='Пароль',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    confirm_password = PasswordField(
        label='Підтвердження паролю',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    submit = SubmitField('Зареєструватися')

    @staticmethod
    def validate_name(username: str):
        username = username.lower()
        user = User.query.filter_by(username=username).first()

        if user:
            raise ValidationError('Ім\'я вже зайняте! Спробуйте використати інше')

    @staticmethod
    def validate_mail(email: str):
        email = email.lower()
        try:
            validate_email(email)
        except Exception:
            raise ValidationError('Неправильний емейл! Спробуйте ще раз')

        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('Емейл вже зайнятий! Спробуйте використати інший')

    @staticmethod
    def password_confirmation(password: str, confirm_password: str):
        if password != confirm_password:
            raise ValidationError('Паролі не збігаються! Спробуйте ще раз')


class LogInForm(FlaskForm):

    username = StringField(
        label='Ім\'я',
        validators=[
            InputRequired(),
            Length(min=2, max=20, message='Ім\'я повинне містити від 2 до 20 символів'),
            Regexp(r'^[a-zA-Z0-9_]*$', message='Ім\'я повинне використовувати тільки латиницю, цифри та підкреслення')
        ]
    )

    password = PasswordField(
        label='Пароль',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    submit = SubmitField('Ввійти')

    @staticmethod
    def validate_name(username: str):
        username = username.lower()
        user = User.query.filter_by(username=username).first()

        if not user:
            raise ValidationError('Користувача не знайдено! Спробуйте ще раз')


class ChangePasswordForm(FlaskForm):

    password = PasswordField(
        label='Старий пароль',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    new_password = PasswordField(
        label='Новий пароль',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    confirm_new_password = PasswordField(
        label='Підтвердження нового паролю',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    submit = SubmitField('Змінити пароль')

    @staticmethod
    def password_confirmation(new_password: str, confirm_new_password: str):
        if new_password != confirm_new_password:
            raise ValidationError('Нові паролі не збігаються! Спробуйте ще раз')


class ResetPassword(FlaskForm):

    new_password = PasswordField(
        label='Новий пароль',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    confirm_new_password = PasswordField(
        label='Підтвердження нового паролю',
        validators=[
            InputRequired(),
            Length(min=8, max=20, message='Пароль повинен містити від 8 до 20 символів')
        ]
    )

    submit = SubmitField('Змінити пароль')
