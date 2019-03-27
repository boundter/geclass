import pytest

from werkzeug.security import check_password_hash
from flask import g, session

from geclass.user_db import UserDB
from geclass.auth import check_valid_email


def test_validate_email():
    assert not check_valid_email('a')
    assert not check_valid_email('ab@cd')
    assert not check_valid_email('ab@cd,de')
    assert not check_valid_email('a b@cd.de')
    assert check_valid_email('ab@cd.de')


def test_register(client, app):
    # register is available
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'email': 'abc@def.gh', 'password': 'a'}
    )
    # after successful register reroute to login
    assert response.headers['Location'] == 'http://localhost/auth/login'

    with app.app_context():
        user_db = UserDB()
        assert user_db.select_user(email="abc@def.gh") is not None


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Eine E-Mail Adresse wird ben\xc3\xb6tigt.'),
    ('abc@de', '', b'Die E-Mail Adresse scheint nicht korrekt zu sein.'),
    ('abc@def.gh', '', b'Ein Passwort wird ben\xc3\xb6tigt.'),
    ('test1@gmail.com', 'test', b'schon registriert.')
))
def test_register_validate_input(client, email, password, message):
    response = client.post(
        '/auth/register',
        data={'email': email, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # login is available
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # login with user test1 leads to user_id 1
    with client:
        client.get('/')
        assert session['user_id'] == 2
        assert g.user['email'] == 'test1@gmail.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a@bc.de', 'bar', b'E-Mail Adresse oder Passwort sind falsch.'),
    ('test1@gmail.com', 'a', b'E-Mail Adresse oder Passwort sind falsch.')
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    # make sure user_id is removed after logout
    with client:
        auth.logout()
        assert 'user_id' not in session


def test_change_email(client, app, auth):
    # non logged in user redirected to log in
    response = client.get('/auth/change_data')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    auth.login()
    # need to change something
    response = client.post(
        '/auth/change_data', data={'email': '', 'password': ''})
    assert b'Entweder eine neue E-Mail Adresse oder ein ' in response.data

    # cannot change both
    response = client.post(
        '/auth/change_data', data={'email': 'ab@cd.ef', 'password': 'a'})
    assert b'Die E-Mail Adresse und das Passwort k\xc3\xb6nn' in response.data

    # can change email
    response = client.post(
        '/auth/change_data', data={'email': 'ab@cd.ef', 'password': ''})
    assert response.headers['Location'] == 'http://localhost/'
    with app.app_context():
        user_db = UserDB()
        assert user_db.select_user(email="ab@cd.ef") is not None

    # can change password
    response = client.post(
        '/auth/change_data', data={'email': '', 'password': 'abc'})
    assert response.headers['Location'] == 'http://localhost/'
    with app.app_context():
        user_db = UserDB()
        assert check_password_hash(
            user_db.select_user(email="ab@cd.ef")['password'], 'abc')


def test_change_pwd_command(auth, runner, client):
    # make sure password is set
    auth.login(email='test2@web.de', password='foo')
    response = client.get('/')
    assert 'Location' not in response.headers
    auth.logout()

    runner.invoke(args=['change-pwd', 'test2@web.de', 'bar'])
    auth.login(email='test2@web.de', password='bar')
    response = client.get('/')
    assert 'Location' not in response.headers
