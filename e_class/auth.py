import functools

from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from e_class.db import DBConnection

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # TODO: Send confirmation link
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        with DBConnection() as db:
            if not email:
                # TODO: Check for valid adress
                error = 'Email adress is required.'
            elif not password:
                error = 'Password is required.'
            elif db.select_user(email=email) is not None:
                error = 'Email adress {} is already registered.'.format(email)

            if error is None:
                db.add_user(email, generate_password_hash(password))
                # TODO: Send directly to landing page
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        with DBConnection() as db:
            user = db.select_user(email=email)

        if user is None:
            error = 'Incorrect Email adress.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.register'))
        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.register'))


@bp.before_app_request
def load_logged_in_user():
    """Load the user data into g."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with DBConnection() as db:
            g.user = db.select_user(user_id=user_id)


def login_required(view):
    """Redirect to login page if not in active session."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
