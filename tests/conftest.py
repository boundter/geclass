"""Handlers for the flask tests."""
import os
import tempfile

import pytest

from geclass import create_app
from geclass.db import DBConnection, init_db


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


@pytest.fixture(autouse=True)
def MonkeyEmail(monkeypatch):
    import geclass.send_email

    class EmailRecorder(object):
        called = False
        recipient = None
        subject = None
        content = None

    def EmailSent(recipient, subject, content):
        EmailRecorder.called = True
        EmailRecorder.recipient = recipient
        EmailRecorder.subject = subject
        EmailRecorder.content = content

    monkeypatch.setattr(geclass.send_email, 'SendEmail', EmailSent)
    return EmailRecorder
