import time
import telebot
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import TOKEN_TELEGRAM
from flask_login import LoginManager

secret = TOKEN_TELEGRAM
bot = telebot.TeleBot(TOKEN_TELEGRAM, threaded=False)

#
# bot.remove_webhook()
# time.sleep(1)
# bot.set_webhook(url="https://1aan.ru/{}".format(secret))
db = SQLAlchemy()
migrate = Migrate(db)
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'main.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)


    from .berrors import bperrors
    app.register_blueprint(bperrors)

    from .btest import bptest
    app.register_blueprint(bptest)

    from .bmain import bpmain
    app.register_blueprint(bpmain)


    from .btelegram import bptelegram
    app.register_blueprint(bptelegram)
    return app


from app import models
