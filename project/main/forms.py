from project import (
    FlaskForm,
    TextAreaField,
    SelectField,
    EmailField,
    SubmitField,
    InputRequired,
    Length,
    ValidationError,
    validate_email
)
from .models import Feedback


class FeedbackForm(FlaskForm):
    sender_email = EmailField(
        label='Електронна пошта',
        validators=[
            InputRequired(),
            Length(min=4, max=100, message='Електронна пошта повинна містити від 4 до 100 символів')
        ]
    )

    body = TextAreaField(
        label='Тіло',
        validators=[
            Length(min=0, max=1000, message='Тіло зворотнього зв\'язку повинне містити до 1000 символів')
        ]
    )

    category = SelectField(
        label='Категорія',
        validators=[InputRequired()],
        choices=[
            ('other', 'Інше'),
            ('question', 'Запитання'),
            ('remark', 'Зауваження'),
            ('recommendation', 'Рекомендація')
        ]
    )

    submit = SubmitField('Надіслати')

    @staticmethod
    def validate_mail(email: str):
        try:
            validate_email(email)
        except Exception:
            raise ValidationError('Неправильний емейл! Спробуйте ще раз')

