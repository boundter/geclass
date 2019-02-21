import pytest

from flask import g, session

from e_class.db import DBConnection


def test_register(client, app):
    # register is available
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'email': 'a', 'password': 'a'}
    )
    # after successful register reroute to login
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        db = DBConnection()
        assert db.select_user(email="a") is not None


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Email adress is required.'),
    ('a', '', b'Password is required.'),
    ('test1', 'test', b'already registered.')
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
    assert 'http://localhost/' == response.headers['Location']

    # login with user test1 leads to user_id 1
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['email'] == 'test1'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'bar', b'Incorrect Email adress.'),
    ('test1', 'a', b'Incorrect password.')
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
