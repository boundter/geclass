from e_class.course_db import CourseDB


def test_only_registered(client, auth):
    # non logged in user redirected to log in
    response = client.get('/')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    # logged in user can acces their overview
    auth.login()
    response = client.get('/')
    assert b'Current Courses' in response.data

    # only own courses appear
    assert b'Bachelor Physiker' in response.data
    assert b'Master Physiker Projekt' in response.data
    assert b'Nebenfach Grundpraktikum' not in response.data


def test_add_new_course(client, app, auth):
    # non logged in user redirected to log in
    response = client.get('/add_course')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    auth.login()
    response = client.post(
        '/add_course',
        data={'name': 'phys_test'})
    # after successfully adding course reroute to index
    assert response.headers['Location'] == 'http://localhost/'

    # check if new course has really been inserted
    with app.app_context():
        course_db = CourseDB()
        assert 'phys_test' in course_db.get_courses(user_id=1)[2]

    # no empty identifiers allowed
    response = client.post(
        '/add_course',
        data={'name': ''})
    assert b'Name is required' in response.data
