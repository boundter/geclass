import os
import sys
import logging

import click
from bs4 import BeautifulSoup
from flask.cli import with_appcontext
import requests

from geclass.send_email import SendEmail

log = logging.getLogger(__name__)

landing_page = "https://survey.uni-potsdam.de/admin.html"
data_page = "https://survey.uni-potsdam.de/admin/export/data/c21d6139/excel/0/0.html"


def GetCSRFToken(html):
    field_id = "login__csrf_token"
    soup = BeautifulSoup(html, "html.parser")
    token = soup.find(id=field_id)["value"]
    return token


@click.command('download-data')
@with_appcontext
def main():
    username = os.environ['QUAMP_USER']
    password = os.environ['QUAMP_PASSWD']
    # TODO: Delte after download
    with requests.Session() as session:
        homepage = session.get(landing_page)
        token = GetCSRFToken(homepage.text)
        response = session.post(
            landing_page,
            data={
                "login[user]": username,
                "login[password]": password,
                "login[_csrf_token]": token,
                "comit": "Anmelden",
            },
        )
        if not "GEClass" in response.text:
            log.error('Could not log in to QUAMP')
            SendEmail(
                'ge-class@uni-potsdam.de',
                'Kein QUAMP einloggen',
                'Der Login bei {} hat nicht funktioniert'.format(landing_page)
            )
            return
        data = session.get(data_page, allow_redirects=True)
        if "GEClass" in data.text:
            SendEmail(
                'ge-class@uni-potsdam.de',
                'Daten konnten nicht von QUAMP geladen werden',
                'Der Download der Daten von {} funktioniert nicht.'
                .format(data_page)
            )
            log.error('Could not download data from QUAMP')
            return
        with open("data.xlsx", "wb") as data_file:
            data_file.write(data.content)


def init_app(app):
    app.cli.add_command(main)
