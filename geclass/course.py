"""Create pages to view and add courses."""
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from geclass.auth import login_required
from geclass.course_db import CourseDB
from geclass.course_question import QuestionText, QuestionNumber, QuestionDropdown, QuestionDropdownWithText

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
        number_experiments = request.form['nr_experiments']
        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            course_db = CourseDB()
            course_db.add_course(session['user_id'], name)
            return redirect(url_for('index'))
        flash(error)
    course_db = CourseDB()
    courses = course_db.execute('SELECT id, name FROM course WHERE user_id = ?', (session['user_id'], )).fetchall()
    questions = (
        QuestionText('name', 'Name', 'Choose a name for your course.'),
        QuestionNumber('nr_exp', 'Number of Experiments',
            'How many experiments are part of the course?', default=0,
            value_range=(0, 100)),
        QuestionDropdown('uni', 'University', 'Where is the course?', courses),
        QuestionDropdownWithText('uni', 'University', 'Where is the course?', courses, 'Other')
            )
    return render_template('course/add_course.html', questions=questions)
