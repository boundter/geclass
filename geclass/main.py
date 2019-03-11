"""Factory for the GEclass webpage."""
import os
import logging

from flask import Flask

logging.basicConfig(level=logging.CRITICAL)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'geclass.sqlite')
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

    return app
