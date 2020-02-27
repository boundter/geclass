import sqlite3

import pytest

import scripts.send_reminder


class MonkeyCourseDB:

    @staticmethod
    def get_surveys_today():
        pre = [{
                    'name' : 'test_pre_1',
                    'user_id' : 1,
                    'identifier' : '12345',
                },
                {
                    'name' : 'test_pre_2',
                    'user_id' : 2,
                    'identifier' : 'abcde',
                    },
            ]
        post = [{
                    'name' : 'test_post_1',
                    'user_id' : 2,
                    'identifier' : '123ab',
                },
                {
                    'name' : 'test_post_2',
                    'user_id' : 1,
                    'identifier' : 'abc12',
                    },
            ]
        return pre, post


class MonkeyUserDB:

    @staticmethod
    def get_email(user_id):
        return user_id


def test_main(monkeypatch, MonkeyEmailList):
    import geclass.course_db
    import geclass.user_db
    monkeypatch.setattr(geclass.course_db, "CourseDB", MonkeyCourseDB)
    monkeypatch.setattr(geclass.user_db, "UserDB", MonkeyUserDB)

    scripts.send_reminder.main()
    assert MonkeyEmailList.called == [True, True, True, True]
    assert MonkeyEmailList.recipient == [1, 2, 2, 1]
    assert MonkeyEmailList.subject == ['Erinnerung GEclass', 'Erinnerung GEclass', 'Erinnerung GEclass', 'Erinnerung GEclass']
    assert 'Prä' in MonkeyEmailList.content[0]
    assert '12345' in MonkeyEmailList.content[0]
    assert 'Prä' in MonkeyEmailList.content[1]
    assert 'abcde' in MonkeyEmailList.content[1]
    assert 'Post' in MonkeyEmailList.content[2]
    assert '123ab' in MonkeyEmailList.content[2]
    assert 'Post' in MonkeyEmailList.content[3]
    assert 'abc12' in MonkeyEmailList.content[3]
