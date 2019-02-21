from flask import Blueprint, render_template, session

from e_class.auth import login_required
from e_class.db import DBConnection

bp = Blueprint(name='course', import_name=__name__)

@bp.route('/')
@login_required
def overview():
    db = DBConnection()
    courses = db.get_courses(session['user_id'])
    return render_template('course/overview.html', courses=courses)
