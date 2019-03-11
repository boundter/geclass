"""Handlers for the flask tests."""
import os
import tempfile

import pytest

from geclass import create_app
from geclass.db import DBConnection, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    DATA_SQL = f.read().decode('utf8')


@pytest.fixture
def app():
    """Create a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        db = DBConnection()
        db().executescript(DATA_SQL)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions():
    def __init__(self, client):
        self._client = client

    def login(self, email='test1@gmail.com', password='test'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
