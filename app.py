# from app import create_app
# app = create_app()
#
# if __name__ == "__main__":
#     app.run(debug=False, host="127.0.0.1", port=5000)


from app import create_app, db, cli
from app.models import User, Question

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question' :Question}