import pytest
from geclass.course_db import CourseDB


def test_only_registered(client, auth):
    # non logged in user redirected to log in
    response = client.get('/')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    # logged in user can acces their overview
    auth.login()
    response = client.get('/')
    assert b'Aktuelle Kurse' in response.data

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
        data={
            'name': 'phys_test',
            'start_date_pre': '2030-03-16',
            'start_date_post': '2031-04-16',
            'university_type': '1',
            'university': '1',
            'program': '1',
            'experience': '1',
            'course_type': '1',
            'traditional': '1',
            'focus': '1',
            'number_students': '20',
            'students_per_instructor': '4',
            'number_experiments': '5',
            'number_projects': '1',
            'lab_per_lecture': '2',
            'hours_per_lab': '2.5',
            'number_labs': '10',
            'week_guided': '1',
            'equipment': '1',
            'frequency_phys_principle': '3',
            'frequency_known_principle': '2',
            'frequency_unknown_principle': '0',
            'students_questions': '0',
            'students_plan': '0',
            'students_design' : '0',
            'students_apparatus' : '0',
            'students_analysis' : '0',
            'students_troubleshoot' : '0',
            'students_groups' : '0',
            'modeling_mathematics' : '0',
            'modeling_model' : '0',
            'modeling_tools' : '0',
            'modeling_measurement' : '0',
            'modeling_predictions' : '0',
            'modeling_uncertainty' : '0',
            'modeling_calibrate' : '0',
            'analysis_uncertainty' : '0',
            'analysis_calculate' : '0',
            'analysis_computer' : '0',
            'analysis_control' : '0',
            'communication_oral' : '0',
            'communication_written' : '0',
            'communication_journal' : '0',
            'communication_lab' : '0',
            'communication_test' : '0',
            'university_free': '',
            'equipment_free': '',
            'notes': ''
            })
    # after successfully adding course reroute to index
    assert response.headers['Location'] == 'http://localhost/'

    # check if new course has really been inserted
    with app.app_context():
        course_db = CourseDB()
        assert 'phys_test' in course_db.get_courses(user_id=2)[2]


@pytest.mark.parametrize(
    ('field', 'value', 'error'),
    (
        ('name', '', b'Name wird ben\xc3\xb6tigt.'),
        ('university', '', b'Hochschule wird ben\xc3\xb6tigt.'),
        ('program', '', b'Studiengang wird ben\xc3\xb6tigt.'),
        ('experience', '', b'Jahrgang wird ben\xc3\xb6tigt.'),
        ('course_type', '', b'Art des Kurses wird ben\xc3\xb6tigt.'),
        ('traditional', '', b'Didaktische Methoden wird ben\xc3\xb6tigt.'),
        ('focus', '', b'Schwerpunkt wird ben\xc3\xb6tigt.'),
        ('number_students', '', b'Anzahl an Studenten wird ben\xc3\xb6tigt.'),
        ('students_per_instructor', '',
            b'Verh\xc3\xa4ltnis Studenten/Betreuer wird ben\xc3\xb6tigt.'),
        ('number_experiments', '', b'Nummer von Experimenten wird ben\xc3\xb6tigt.'),
        ('number_projects', '', b'Nummer von Projekten wird ben\xc3\xb6tigt.'),
        ('equipment', '', b'Ger\xc3\xa4te wird ben\xc3\xb6tigt.'),
        ('start_date_pre', '', b'Start Pr\xc3\xa4-Befragung wird ben\xc3\xb6tigt.'),
        ('start_date_post', '', b'Start Post-Befragung wird ben\xc3\xb6tigt.'),
        ('start_date_pre', '2010-09-09',
            b'Das Anfangsdatum muss in der Zukunft liegen.'),
        ('start_date_post', '2010-09-09',
            b'Das Anfangsdatum muss in der Zukunft liegen.'),
        ('start_date_post', '2030-03-15',
            b'Start Post-Befragung muss nach der Pre-Befragung sein.')
    )
)
def test_add_new_course_missing_value(client, auth, field, value, error):
    data={
        'name': 'phys_test',
        'program': '1',
        'course_type': '1',
        'focus': '1',
        'traditional': '1',
        'equipment': '1',
        'experience': '1',
        'university': '1',
        'number_students': '20',
        'students_per_instructor': '4',
        'lab_per_lecture': '2',
        'number_experiments': '5',
        'number_projects': '1',
        'start_date_pre': '2030-03-16',
        'start_date_post': '2031-04-16',
        'university_free': '',
        'equipment_free': '',
        'notes': ''
        }

    auth.login()
    data[field] = value
    response = client.post('/add_course', data=data)
    assert error in response.data


