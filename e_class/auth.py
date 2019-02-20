from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from e_class.db import get_db

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # TODO: Send confirmation link
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            # TODO: Check for valid adress
            error = 'Email adress is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email adress {} is already registered.'.format(email)

        if error is None:
            db.execute('INSERT INTO user (email, password) VALUES (?, ?)',
                (email, generate_password_hash(password)))
            db.commit()
            # TODO: Send directly to landing page
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

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
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    """Redirect to login page if not in active session."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
