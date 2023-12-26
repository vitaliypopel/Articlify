from flask import Blueprint, render_template, flash

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('main/home.html')


@views.route('/favicon.ico')
def favicon():
    return 'icon'
