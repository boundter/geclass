"""Handlers for the flask tests."""
import os
import sys
import tempfile
import logging
import datetime
import time

from flask import current_app
import pytest

from geclass import create_app
from geclass.db import DBConnection, init_db, DBConnection


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
        _db = DBConnection()
        with current_app.open_resource('../tests/data.sql') as f:
            _db().executescript(f.read().decode('utf8'))

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


@pytest.fixture
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


@pytest.fixture
def MonkeyEmailList(monkeypatch):
    import geclass.send_email

    class EmailRecorder(object):
        called = []
        recipient = []
        subject = []
        content = []

    def EmailSent(recipient, subject, content):
        EmailRecorder.called.append(True)
        EmailRecorder.recipient.append(recipient)
        EmailRecorder.subject.append(subject)
        EmailRecorder.content.append(content)

    monkeypatch.setattr(geclass.send_email, 'SendEmail', EmailSent)
    return EmailRecorder

@pytest.fixture
def MonkeyDBDates(monkeypatch):
    import geclass.db

    class DatesContainer(object):
        start_date_pre = str(int(
            time.mktime(datetime.date(2001, 1, 5).timetuple())))
        start_date_post = str(int(
            time.mktime(datetime.date(2002, 1, 20).timetuple())))

        def fetchall(self):
            return [(self.start_date_pre, self.start_date_post)]

    def MockExec(obj, query, identifier):
        return DatesContainer()

    monkeypatch.setattr(geclass.DBConnection, 'execute', MockExec)
    return DatesContainer


@pytest.fixture(autouse=True)
def NoLogging(caplog):
    caplog.set_level(logging.DEBUG)

    yield

    caplog.clear()
