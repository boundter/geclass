"""Test the db functionality for the GEclass."""
import sqlite3

import pytest
from flask import g

from geclass.db import DBConnection


def test_get_close_db(app):
    with app.app_context():
        db = DBConnection()
        assert db() is g.db

    # after the context the db connection gets teared down
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute('SELECT 1')


def test_init_db_command(runner, monkeypatch):
    init = {'called': False}

    def fake_init_db():
        init['called'] = True

    monkeypatch.setattr('geclass.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert init['called']
