"""Create pages to view and add courses."""
from datetime import date
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from geclass.auth import login_required
from geclass.course_db import CourseDB
from geclass.course_question import CreateQuestions

log = logging.getLogger(__name__)

bp = Blueprint(name='course', import_name=__name__)


@bp.route('/')
@login_required
def overview():
    course_db = CourseDB()
    courses = course_db.get_overview(session['user_id'])
    log.debug('course = %s', courses)
    return render_template('course/overview.html', courses=courses)


@bp.route('/add_course', methods=('GET', 'POST'))
@login_required
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        number_experiments = request.form['nr_experiments']
        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            course_db = CourseDB()
            course_db.add_course(session['user_id'], name)
            return redirect(url_for('index'))
        flash(error)
    questions = CreateQuestions()
    return render_template('course/add_course.html', questions=questions)
