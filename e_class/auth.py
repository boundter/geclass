"""Create pages to login, register and change user data.

Aside from the pages there are also some utility functions. The most
important one checks, if the current user is logged in and redirects
to the log-in page if needed.
"""
# TODO: Check if email already registered

import functools
import re
import logging

import click
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.cli import with_appcontext

from e_class.db import DBConnection

log = logging.getLogger(__name__)

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


def check_valid_email(email):
    """Check if the given email has a valid form.

    Args:
        email (str): The email adress to check.

    Returns:
        A bool containing the validity.
    """
    return re.match(r'[^ @]+@[^ @]+\.[^ @]+', email) is not None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # TODO: Send confirmation link
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        db = DBConnection()

        if not email:
            error = 'Email adress is required.'
        elif not check_valid_email(email):
            error = 'Email adress does not seem to be valid.'
        elif not password:
            error = 'Password is required.'
        elif db.select_user(email=email) is not None:
            error = 'Email adress {} is already registered.'.format(email)

        if error is None:
            db.add_user(email, generate_password_hash(password))
            return redirect(url_for('auth.login'))
        log.info('Invalid registration with email {}'.format(email))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        db = DBConnection()
        user = db.select_user(email=email)

        if user is None:
            error = 'Incorrect Email adress.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            log.info(
                'Incorrect password entry by user {}'.format(user['id']))

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            logging.info('User {} logged in'.format(user['id']))
            return redirect(url_for('index'))
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
        db = DBConnection()
        g.user = db.select_user(user_id=user_id)


def login_required(view):
    """Redirect to login page, if not logged in.

    This can be used as a decorator, to only allow logged in users
    to access a page.

    ::

        @bp.route('/test')
        @login_required
        def test_page():
            return rendender_template('/test.html')

    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/change_data', methods=('GET', 'POST'))
@login_required
def change_data():
    if request.method == 'POST':
        # TODO: Reenter password
        email = request.form['email']
        password = request.form['password']
        error = None

        if not (email or password):
            error = 'Email adress or password is needed.'
        elif email and password:
            error = 'The Email and password cannot be ' + \
                    'changed at the same time.'
        elif email:
            if not check_valid_email(email):
                error = 'Email adress does not seem to be valid.'

        if error is None:
            db = DBConnection()
            if email:
                db.change_email(user_id=session['user_id'], email=email)
            else:
                db.change_password(
                    user_id=session['user_id'],
                    password=generate_password_hash(password))
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/change_data.html')


@click.command('change-pwd')
@click.argument('email')
@click.argument('new_password')
@with_appcontext
def change_pwd_command(email, new_password):
    """Create CLI to change the password of a user.

    Sometime a user may loose their password. It can be set to a given
    value by calling `flask change-pwd email new_password`.

    """
    db = DBConnection()
    user = db.select_user(email=email)
    log.info(
        'Force password change for user {} with email {}'
        ''.format(user['id'], user['email']))
    db.change_password(
        user_id=user['id'], password=generate_password_hash(new_password))


def change_pwd(app):
    app.cli.add_command(change_pwd_command)

