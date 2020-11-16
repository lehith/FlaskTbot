from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    total_question = db.Column(db.Integer)
    good_question = db.Column(db.Integer)
    fail_question = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text)
    question_answer = db.Column(db.Text)
    question_answer_varian1 = db.Column(db.Text)
    question_answer_varian2 = db.Column(db.Text)
    question_answer_varian3 = db.Column(db.Text)
    question_answer_varian4 = db.Column(db.Text)
    question_answer_varian5 = db.Column(db.Text)
    question_answer_varian6 = db.Column(db.Text)

    def __str__(self):
        return '<Question: {}>'.format(self.question_text)

    def check(self, answer):
        if str(answer) == str(self.question_answer):
            return True
        else:
            return False

    def findansw(self):
        if str(self.question_answer) == str(self.question_answer_varian1):
            return 0
        elif str(self.question_answer) == str(self.question_answer_varian2):
            return 1
        elif str(self.question_answer) == str(self.question_answer_varian3):
            return 2
        elif str(self.question_answer) == str(self.question_answer_varian4):
            return 3
        elif str(self.question_answer) == str(self.question_answer_varian5):
            return 4
        elif str(self.question_answer) == str(self.question_answer_varian6):
            return 5
        else:
            return 10
