"""Create pages to view and add courses."""
from datetime import date, datetime
import logging
import os

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app, send_from_directory
)

from geclass.auth import login_required
from geclass.course_db import CourseDB
from geclass.course_question import HandleCourseQuestions

log = logging.getLogger(__name__)

bp = Blueprint(name='course', import_name=__name__)


@bp.route('/report/<string:course_name>.pdf')
@login_required
def send_pdf(course_name):
    report_dir = os.path.join(current_app.instance_path, course_name)
    return send_from_directory(report_dir, 'report.pdf')


@bp.route('/')
@login_required
def overview():
    course_db = CourseDB()
    courses = course_db.get_overview(session['user_id'])
    past_courses = []
    current_courses = []
    for course in courses:
        course_post = datetime.strptime(course[7], '%d.%m.%Y').date()
        if course_post < date.today():
            report_dir = os.path.join(current_app.instance_path, course[0])
            if os.path.exists(report_dir):
                course = list(course) + [course[0]]
            past_courses.append(course)
        else:
            current_courses.append(course)
    return render_template(
        'course/overview.html', current_courses=current_courses,
        past_courses=past_courses)


@bp.route('/add_course', methods=('GET', 'POST'))
@login_required
def add_course():
    questions = HandleCourseQuestions()
    if request.method == 'POST':
        log.debug('Add new course with form: %s', request.form)

        errors = questions.parse(request.form)

        if not errors:
            questions.write(session['user_id'])
            return redirect(url_for('index'))

        for error in errors:
            flash(error)
    return render_template('course/add_course.html', questions=questions)
