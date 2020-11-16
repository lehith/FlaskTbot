from random import randint
from flask import request, render_template, flash
from flask_login import login_required, current_user
from app import db
from app.models import Question, User

from flask import Blueprint

bptest = Blueprint('test', __name__)


@bptest.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    buttonnext = False
    buttongreen = 10
    buttonred = 10
    if request.method == 'POST':
        if request.values.get('answer'):
            user = User.query.filter_by(username=str(current_user.username).lower()).first()
            question = Question.query.filter_by(id=request.values.get('id')).first()
            buttonnum = int(request.values.get('button'))
            user.total_question += 1
            if question.check(request.values.get('answer')):
                user.good_question += 1
                db.session.commit()
                buttongreen = buttonnum
                # flash('Вы ответили верно . Всего ответов:{}, верных ответов:{}, неверных ответов:{}' \
                #       .format(user.total_question, user.good_question, user.fail_question))
            else:
                user.fail_question += 1
                db.session.commit()
                buttonred = buttonnum
                buttongreen = question.findansw()

                # flash('Вы ответили не верно . Всего ответов:{}, верных ответов:{}, неверных ответов:{}' \
                #       .format(user.total_question, user.good_question, user.fail_question))
            buttonnext = True
        elif request.values.get('nextQuest') == 'next':
            question = Question.query.filter_by(id=int(request.values.get('id')) + 1).first()
        else:
            row = Question.query.count()
            question = Question.query.filter_by(id=randint(1, row)).first()

    if request.method == 'GET':
        row = Question.query.count()
        question = Question.query.filter_by(id=randint(1, row)).first()

    buttons = [
        {'id': 0, 'ans': question.question_answer_varian1, 'color': "blue"},
        {'id': 1, 'ans': question.question_answer_varian2, 'color': "blue"},
        {'id': 2, 'ans': question.question_answer_varian3, 'color': "blue"},
        {'id': 3, 'ans': question.question_answer_varian4, 'color': "blue"},
        {'id': 4, 'ans': question.question_answer_varian5, 'color': "blue"},
        {'id': 5, 'ans': question.question_answer_varian6, 'color': "blue"},
    ]
    if buttongreen < 10:
        buttons[buttongreen]["color"] = "green"
    if buttonred < 10:
        buttons[buttonred]["color"] = "red"

    return render_template('test.html', title='test', question=question,
                           buttonnext=buttonnext,
                           buttons=buttons)
