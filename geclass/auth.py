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

from geclass.user_db import UserDB

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
        user_db = UserDB()

        if not email:
            error = 'Eine E-Mail Adresse wird benötigt.'
        elif not check_valid_email(email):
            error = 'Die E-Mail Adresse scheint nicht korrekt zu sein.'
        elif not password:
            error = 'Ein Passwort wird benötigt.'
        elif user_db.select_user(email=email) is not None:
            error = 'Die E-Mail Adresse {} ist schon registriert.'.format(email)

        if error is None:
            user_db.add_user(email, generate_password_hash(password))
            return redirect(url_for('auth.login'))
        log.info('Invalid registration with email %s', email)
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user_db = UserDB()
        user = user_db.select_user(email=email)

        if user is None:
            error = 'E-Mail Adresse oder Passwort sind falsch.'
        elif not check_password_hash(user['password'], password):
            error = 'E-Mail Adresse oder Passwort sind falsch.'
            log.info('Incorrect password entry by user %s', user['id'])

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            log.info('User %s logged in', user['id'])
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
        user_db = UserDB()
        g.user = user_db.select_user(user_id=user_id)


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
            error = 'Entweder eine neue E-Mail Adresse oder ein neues ' + \
                    'Passwort müssen geetzt werden.'
        elif email and password:
            error = 'Die E-Mail Adresse und das Passwort können nicht ' + \
                    'zur selben Zeit geändert werden.'
        elif email:
            if not check_valid_email(email):
                error = 'Die E-Mail Adresse scheint nicht korrekt zu sein.'

        if error is None:
            user_db = UserDB()
            if email:
                user_db.change_email(
                    user_id=session['user_id'], new_email=email)
            else:
                user_db.change_password(
                    user_id=session['user_id'],
                    new_password=generate_password_hash(password))
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
    user_db = UserDB()
    user = user_db.select_user(email=email)
    log.info(
        'Force password change for user %s with email %s',
        user['id'], user['email'])
    user_db.change_password(
        user_id=user['id'], new_password=generate_password_hash(new_password))


def change_pwd(app):
    app.cli.add_command(change_pwd_command)
