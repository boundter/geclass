import pytest
import datetime
from datetime import date
import time

from geclass.course_db import CourseDB


def test_select_all_courses(app):
    with app.app_context():
        course_db = CourseDB()
        courses = course_db.get_courses(user_id=2)
        assert courses[0]['name'] == 'Bachelor Physiker'
        assert courses[1]['name'] == 'Master Physiker Projekt'


def test_add_course(app, MonkeyEmail):
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
        assert MonkeyEmail.called
        assert MonkeyEmail.recipient == 'test1@gmail.com'
        assert MonkeyEmail.subject == 'Kurs Registrierung GEclass'
        assert course_name in MonkeyEmail.content


def test_get_surveys_today(app, MonkeyEmail):
    with app.app_context():
        timestamp_today = str(int(time.mktime(date.today().timetuple())))
        fields_pre = {
            'name': 'test_pre',
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
            'start_date_pre': timestamp_today,
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
        fields_post_1 = fields_pre.copy()
        fields_post_1['name'] = 'test_post_1'
        fields_post_1['start_date_pre'] = 1
        fields_post_1['start_date_post'] = timestamp_today
        fields_post_2 = fields_post_1.copy()
        fields_post_2['name'] = 'test_post_2'
        course_db = CourseDB()
        course_db.generate_identifier = lambda: '12345'
        course_db.add_course(user_id=1, fields=fields_pre)
        course_db.add_course(user_id=1, fields=fields_post_1)
        course_db.add_course(user_id=2, fields=fields_post_2)
        pre, post = course_db.get_surveys_today()
        pre_list = []
        for row in pre:
            pre_list.append(list(row))
        post_list = []
        for row in post:
            post_list.append(list(row))
        assert [1, 'test_pre', '12345'] in pre_list
        assert [1, 'test_post_1', '12345'] in post_list
        assert [2, 'test_post_2', '12345'] in post_list


def test_get_course_dates(app, MonkeyDBDates):
    with app.app_context():
        course_db = CourseDB()
        times = course_db.get_course_questionnaire_dates(1)
        # dummy values from conftest.py
        start_date_pre = str(int(
            time.mktime(datetime.date(2001, 1, 5).timetuple())))
        start_date_post = str(int(
            time.mktime(datetime.date(2002, 1, 20).timetuple())))
        assert times["pre"] == start_date_pre
        assert times["post"] == start_date_post


def test_get_course_id(app):
    with app.app_context():
        identifiers = {'abxce': 1, 'tryui': 2, 'oiuyt': 3, 'ertyu': 4}
        course_db = CourseDB()
        for key in identifiers:
            course_id = course_db.get_course_id(key)
            assert course_id[0] == identifiers[key]


def test_get_similar_course(app):
    with app.app_context():
        similar = {1: [4], 2: [None], 3: [None], 4: [1]}
        course_db = CourseDB()
        for key in similar:
            similar_ids = course_db.get_similar_course_ids(key)
            for indx, val in enumerate(similar_ids):
                assert val[0] == similar[key][indx]


def test_course_report_info(app):
    with app.app_context():
        results = {
            1: ['Bachelor Physiker', 32],
            2: ['Master Physiker Projekt', 16],
            3: ['Nebenfach Grundpraktikum', 25],
            4: ['Bachelor Physiker 2', 25],
        }
        course_db = CourseDB()
        for key in results:
            info = course_db.get_course_report_info(key)
            assert info[0] == results[key][0]
            assert info[1] == results[key][1]

