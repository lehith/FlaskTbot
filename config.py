import os
basedir = os.path.abspath(os.path.dirname(__file__))


TOKEN_TELEGRAM = '1095386139:AAEuGsPPy8kcPFMt2gfXSHV-vgFUzGSdl-Q'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False