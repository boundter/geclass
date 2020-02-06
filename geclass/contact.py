from flask import Blueprint, render_template

bp = Blueprint(name='contact', import_name=__name__, url_prefix='/contact')

@bp.route('/')
def contact():
    return render_template('contact.html')
