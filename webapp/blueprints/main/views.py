from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/home')
@login_required
def home():

    return render_template('main/home.html')
