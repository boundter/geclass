from flask import Blueprint, render_template

from e_class.auth import login_required

bp = Blueprint(name='course', import_name=__name__)

@bp.route('/')
@login_required
def overview():
    return render_template('course/overview.html')
