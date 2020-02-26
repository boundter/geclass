import pytest

from geclass.course_db import CourseDB


@pytest.fixture(autouse=True)
def MonkeyEmail(monkeypatch):
    import geclass.send_email

    def EmailSent(recipient, subject, content):
        return None

    monkeypatch.setattr(geclass.send_email, 'SendEmail', EmailSent)


def test_select_all_courses(app):
    with app.app_context():
        course_db = CourseDB()
        courses = course_db.get_courses(user_id=2)
        assert courses[0]['name'] == 'Bachelor Physiker'
        assert courses[1]['name'] == 'Master Physiker Projekt'


def test_add_course(app):
    with app.app_context():
        course_db = CourseDB()
        courses = course_db.get_courses(user_id=2)
        assert len(courses) == 2
        course_name = 'New Course'
        fields = {
            'name': course_name,
            'program_id': '1',
            'course_type_id': '1',
            'focus_id': '1',
            'traditional_id': '1',
            'equipment_id': '1',
            'experience_id': '1',
            'university_type_id': '1',
            'university_id': '1',
            'number_students': '20',
            'students_per_instructor': '4',
            'lab_per_lecture': '2',
            'hours_per_lab': '2.5',
            'number_labs': '10',
            'number_experiments': '5',
            'number_projects': '1',
            'week_guided': '1',
            'start_date_pre': '1899849600',
            'start_date_post': '1934064000',
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
            'communication_lab' : '0',
            'communication_journal' : '0',
            'communication_test': '0'
            }
        course_db.add_course(user_id=2, fields=fields)
        courses = course_db.get_courses(user_id=2)
        assert len(courses) == 3
        assert courses[-1]['name'] == course_name
