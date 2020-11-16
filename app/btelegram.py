from random import randint
from flask import request
from telebot import types

from app import  secret, bot, db
from app.models import User, Question
from flask import Blueprint

bptelegram = Blueprint('telegram', __name__)

@bptelegram.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


@bot.message_handler(commands=['start', 'help'])
def startCommand(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('/next', 'cancel')
    bot.send_message(message.chat.id, 'Привет *' + message.chat.first_name + "*, для того чтобы начать получать вопросы отправь '/next'\
                    для просмотра статистики перейди https://1aan.ru . логин твой ник в телеге, пароль 1", reply_markup=markup)


@bot.message_handler(commands=['next'])
def send_question(message):
    try:
        row = Question.query.count()
        question = Question.query.filter_by(id=randint(1, row)).first()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtna = types.KeyboardButton(question.question_answer_varian1)
        itembtnb = types.KeyboardButton(question.question_answer_varian2)
        itembtnc = types.KeyboardButton(question.question_answer_varian3)
        itembtnd = types.KeyboardButton(question.question_answer_varian4)
        itembtne = types.KeyboardButton(question.question_answer_varian5)
        itembtnf = types.KeyboardButton(question.question_answer_varian6)
        markup.row(itembtna, itembtnb, itembtnc)
        markup.row(itembtnd, itembtne, itembtnf)
        msg = bot.send_message(message.chat.id, str(question.question_text), reply_markup=markup,
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, process_answer_step, questid=question.id)
    except Exception as e:
        bot.reply_to(message, 'Something wrong!')


def process_answer_step(message, questid):
    try:
        # user = User.query.filter_by(username=message.chat.first_name).first()
        user = checkUser(message.chat.first_name)
        question = Question.query.filter_by(id=questid).first()
        user.total_question += 1
        if question.check(message.text):
            user.good_question += 1
            db.session.commit()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('/next', 'cancel')
            bot.send_message(message.chat.id, 'Правильно, всего:{}, верно:{}, не верно:{}' \
                             .format(user.total_question, user.good_question, user.fail_question), reply_markup=markup)
        else:
            raise Exception()

    except Exception as e:
        user.fail_question += 1
        db.session.commit()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('/next', 'cancel')
        bot.send_message(message.chat.id, 'Ooops , верный ответ : {}, всего:{}, верно:{}, не верно:{}' \
                         .format(question.question_answer, user.total_question, user.good_question, user.fail_question),
                         reply_markup=markup)


def checkUser(username):
    user = User.query.filter_by(username=username.lower()).first()
    if user is None:
        user = User(username=username.lower(), total_question=0, good_question=0, fail_question=0)
        user.set_password("1")
        db.session.add(user)
        db.session.commit()
    return user
