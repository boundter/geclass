"""Functions to access the web-database."""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Get connection to database and create new one, if none exists."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            database=current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    # e is needed for the teardown and is needed for an error object
    db = g.pop(name='db', default=None)
    if db is not None:
        db.close()


def init_db():
    """Remove old database (if exists) and create new one."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Remove old database (if exists) and create new one."""
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    """Connection to factory."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
