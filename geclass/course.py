"""Create pages to view and add courses."""
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from geclass.auth import login_required
from geclass.course_db import CourseDB
from geclass.course_question import HandleCourseQuestions

log = logging.getLogger(__name__)

bp = Blueprint(name='course', import_name=__name__)


@bp.route('/')
@login_required
def overview():
    course_db = CourseDB()
    courses = course_db.get_overview(session['user_id'])
    return render_template('course/overview.html', courses=courses)


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
