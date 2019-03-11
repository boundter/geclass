"""Create pages to view and add courses."""
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from geclass.auth import login_required
from geclass.course_db import CourseDB

log = logging.getLogger(__name__)

bp = Blueprint(name='course', import_name=__name__)


@bp.route('/')
@login_required
def overview():
    course_db = CourseDB()
    courses = course_db.get_courses(session['user_id'])
    return render_template('course/overview.html', courses=courses)


@bp.route('/add_course', methods=('GET', 'POST'))
@login_required
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            course_db = CourseDB()
            course_db.add_course(session['user_id'], name)
            return redirect(url_for('index'))
        flash(error)
    return render_template('course/add_course.html')
