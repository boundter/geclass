"""Factory for the GEclass webpage."""
import os
import logging

from flask import Flask

logging.basicConfig(filename='/var/log/geclass/geclass.log', level=logging.INFO)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if 'FLASK_KEY' in os.environ and os.environ['FLASK_KEY'] != '':
        key = os.environ['FLASK_KEY']
    else:
        key = 'dev'
    app.config.from_mapping(
        SECRET_KEY=key,
        DATABASE=os.path.join(app.instance_path, 'geclass.sqlite'),
        QUESTIONNAIRE_DB=os.path.join(app.instance_path, 'questionnaire.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.change_pwd(app)

    from . import course
    app.register_blueprint(course.bp)
    app.add_url_rule('/', endpoint='index')

    from . import contact
    app.register_blueprint(contact.bp)

    from .util import send_reminder
    send_reminder.init_app(app)

    from .util import report
    report.init_app(app)

    from .util import questionnaire_db
    questionnaire_db.init_app(app)

    return app
