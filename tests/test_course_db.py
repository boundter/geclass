from geclass.course_db import CourseDB


def test_select_all_courses(app):
    with app.app_context():
        course_db = CourseDB()
        courses = course_db.get_courses(user_id=1)
        assert courses[0]['name'] == 'Bachelor Physiker'
        assert courses[1]['name'] == 'Master Physiker Projekt'


def test_add_course(app):
    with app.app_context():
        course_db = CourseDB()
        courses = course_db.get_courses(user_id=1)
        assert len(courses) == 2
        course_name = 'New Course'
        course_db.add_course(user_id=1, course_name=course_name)
        courses = course_db.get_courses(user_id=1)
        assert len(courses) == 3
        assert courses[-1]['name'] == course_name
