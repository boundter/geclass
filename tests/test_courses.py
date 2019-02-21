from flask import session

from e_class.db import DBConnection

def test_only_registered(client, auth):
    # non logged in user redirected to log in
    response = client.get('/')
    assert 'http://localhost/auth/login' == response.headers['Location']

    # logged in user can acces their overview
    auth.login()
    response = client.get('/')
    print(response.data)
    print(response.headers)
    assert b'Your courses' in response.data

    # only own courses appear
    assert b'uni_potsdam_biochem_2018' in response.data
    assert b'uni_potsdam_phys_2018' in response.data
    assert b'uni_hamburg_phys_2018' not in response.data


def test_add_new_course(client, app, auth):
    # non logged in user redirected to log in
    response = client.get('/add_course')
    assert 'http://localhost/auth/login' == response.headers['Location']

    auth.login()
    response = client.post(
        '/add_course',
        data={'identifier': 'phys_test'})
    # after successfully adding course reroute to index
    assert 'http://localhost/' == response.headers['Location']

    # check if new course has really been inserted
    with app.app_context():
        db = DBConnection()
        assert 'phys_test' in db.get_courses(user_id=1)[2]

    # no empty identifiers allowed
    response = client.post(
        '/add_course',
        data={'identifier': ''})
    assert b'Identifier is required' in response.data


