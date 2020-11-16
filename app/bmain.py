from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from app import  db
from app.forms import LoginForm, RegistrationForm
from app.models import Question, User
from flask_login import current_user, login_user, logout_user, login_required

from flask import Blueprint

bpmain = Blueprint('main', __name__)

@bpmain.route('/')
@bpmain.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bpmain.route('/question')
@login_required
def question():
    questions = Question.query.order_by(Question.id.asc()).all()
    return render_template('question.html', title='question', questions=questions)


@bpmain.route('/statistic')
@login_required
def statistic():
    users = User.query.order_by(User.id.asc()).all()
    return render_template('statistic.html', title='статистика', users=users)


@bpmain.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bpmain.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bpmain.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), total_question=0,
                    good_question=0, fail_question=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@bpmain.route('/reset_password_request')
def reset_password_request():
    pass

