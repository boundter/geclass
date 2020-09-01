import pandas as pd
import click

from flask.cli import with_appcontext

from geclass.questionnaire_prepare import PrepareData
from geclass.questionnaire_db import QuestionnaireDB

@click.command('load-questionnaire-data')
@click.argument('file_location')
@with_appcontext
def load_questionnaire_data(file_location):
    data = pd.read_excel(file_location)
    df = PrepareData(data)
    questionnaire_db = QuestionnaireDB()
    questionnaire_db.insert_data(df)
    click.echo('Loaded questionnaire data')


def init_app(app):
    app.cli.add_command(load_questionnaire_data)
