"""Create pages to view and add courses."""
import logging

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from e_class.auth import login_required
from e_class.db import DBConnection

log = logging.getLogger(__name__)

bp = Blueprint(name='course', import_name=__name__)


@bp.route('/')
@login_required
def overview():
    db = DBConnection()
    courses = db.get_courses(session['user_id'])
    return render_template('course/overview.html', courses=courses)


@bp.route('/add_course', methods=('GET', 'POST'))
@login_required
def add_course():
    if request.method == 'POST':
        identifier = request.form['identifier']
        error = None

        if not identifier:
            error = 'Identifier is required.'

        if error is None:
            db = DBConnection()
            db.add_course(session['user_id'], identifier)
            return redirect(url_for('index'))
        flash(error)
    return render_template('course/add_course.html')
