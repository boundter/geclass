"""Test the db functionality for the GEclass."""
import sqlite3

import pytest
from flask import g
import pandas as pd
import datetime
import time

from geclass.util.questionnaire_db import QuestionnaireDB


def test_get_close_db(app):
    with app.app_context():
        db = QuestionnaireDB()
        assert db() is g.questionnaire_db

    # after the context the db connection gets teared down
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT 1')


def test_init_db_command(runner, monkeypatch):
    init = {'called': False}

    def fake_init_db():
        init['called'] = True

    monkeypatch.setattr('geclass.util.questionnaire_db.init_questionnaire_db', fake_init_db)
    result = runner.invoke(args=['init-questionnaire-db'])
    assert 'Initialized' in result.output
    assert init['called']

def test_insert_data(app, MonkeyCourseDBCourses):
    data = {
        'personal_code': ['a', 'a', 'b', 'a'],
        'course_id': [1, 1, 1, 0],
        'pre_post': [1, 2, 2, 1],
        'valid_control': [True, False, True, True],
        'valid_time': [False, True, True, True],
    }
    len_data = len(data['personal_code'])
    data['start'] = [datetime.datetime.today() for _ in range(len_data)]
    data['end'] = [datetime.datetime.today() for _ in range(len_data)]
    start = int(time.mktime(data['start'][0].timetuple()))
    end = int(time.mktime(data['end'][0].timetuple()))
    for i in range(1, 31):
        data['q{:d}_1'.format(i)] = [1 for _ in range(len_data)]
        data['q{:d}_2'.format(i)] = [1 for _ in range(len_data)]
    for i in range(1, 24):
        data['post_{:d}'.format(i)] = [1 for _ in range(len_data)]
    df = pd.DataFrame(data=data)
    with app.app_context():
        questionnaire_db = QuestionnaireDB()
        questionnaire_db.insert_data(df)
        students = list(questionnaire_db.select_all_entries('student'))
        students_list = []
        for row in students:
            students_list.append(list(row))
        assert students_list[0] == [1, 'a']
        assert students_list[1] == [2, 'b']
        assert students_list[2] == [3, 'a']
        student_course = list(questionnaire_db.select_all_entries('student_course'))
        student_course_list = []
        for row in student_course:
            student_course_list.append(list(row))
        assert student_course_list[0] == [1, 1, 1]
        assert student_course_list[1] == [2, 2, 1]
        student_unknown = list(questionnaire_db.select_all_entries('student_unknown_course'))
        student_unknown_list = []
        for row in student_unknown:
            student_unknown_list.append(list(row))
        assert student_unknown_list[0] == [1, 3, '0']
        q_pre = list(questionnaire_db.select_all_entries('questionnaire_pre'))
        q_pre_list = []
        for row in q_pre:
            q_pre_list.append(list(row))
        assert q_pre_list[0] == [1, 1, 1]
        assert q_pre_list[1] == [2, 4, 4]
        q_post = list(questionnaire_db.select_all_entries('questionnaire_post'))
        q_post_list = []
        for row in q_post:
            q_post_list.append(list(row))
        assert q_post_list[0] == [1, 2, 2, 1]
        assert q_post_list[1] == [2, 3, 3, 2]
        s_pre = list(questionnaire_db.select_all_entries('student_pre'))
        s_pre_list = []
        for row in s_pre:
            s_pre_list.append(list(row))
        assert s_pre_list[0] == [1, 1, 1, start, end, 1, 0]
        assert s_pre_list[1] == [2, 3, 2, start, end, 1, 1]
        s_post = list(questionnaire_db.select_all_entries('student_post'))
        s_post_list = []
        for row in s_post:
            s_post_list.append(list(row))
        assert s_post_list[0] == [1, 1, 1, start, end, 0, 1]
        assert s_post_list[1] == [2, 2, 2, start, end, 1, 1]

