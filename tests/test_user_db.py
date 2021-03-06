import pytest

from geclass.user_db import UserDB


def test_select_user(app):
    with app.app_context():
        user_db = UserDB()
        user_id = user_db.select_user(user_id=2)
        email = user_db.select_user(email='test1@gmail.com')
        no_entry = user_db.select_user(email='ab@uz.com')
        assert user_id['email'] == 'test1@gmail.com'
        assert email['id'] == 2
        assert no_entry is None


def test_add_user(app, MonkeyEmail):
    with app.app_context():
        user_db = UserDB()
        email = 'gp@uni-potsdam.de'
        password = 'abc'
        user_db.add_user(email=email, encrypted_password=password)
        user_id = user_db.select_user(email='gp@uni-potsdam.de')
        assert user_id is not None
        assert MonkeyEmail.called
        assert MonkeyEmail.recipient == email
        assert MonkeyEmail.subject == 'Registrierung für die GEclass'
        assert 'registriert haben' in MonkeyEmail.content


def test_change_email(app):
    with app.app_context():
        user_db = UserDB()
        new_email = 'gp@uni-potsdam.de'
        user = user_db.select_user(user_id=2)
        assert user['email'] != new_email
        user_db.change_email(user_id=2, new_email=new_email)
        user = user_db.select_user(user_id=2)
        assert user['email'] == new_email


def test_change_password(app):
    with app.app_context():
        user_db = UserDB()
        new_password = 'abc'
        user = user_db.select_user(user_id=2)
        assert user['password'] != new_password
        user_db.change_password(user_id=2, new_password=new_password)
        user = user_db.select_user(user_id=2)
        assert user['password'] == new_password


def test_get_email(app):
    with app.app_context():
        user_db = UserDB()
        user_id = 2
        email = user_db.get_email(user_id)
        assert email == 'test1@gmail.com'
