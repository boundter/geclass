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
        fields = {
            'name': course_name,
            'program_id': '1',
            'course_type_id': '1',
            'focus_id': '1',
            'traditional_id': '1',
            'equipment_id': '1',
            'experience_id': '1',
            'university_id': '1',
            'number_students': '20',
            'students_per_instructor': '4',
            'lab_per_lecture': '2',
            'number_experiments': '5',
            'number_projects': '1',
            'start_date_pre': '2030-03-16',
            'start_date_post': '2031-04-16'
            }
        course_db.add_course(user_id=1, fields=fields)
        courses = course_db.get_courses(user_id=1)
        assert len(courses) == 3
        assert courses[-1]['name'] == course_name
