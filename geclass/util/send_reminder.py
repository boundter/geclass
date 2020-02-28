import click
from flask.cli import with_appcontext

import geclass.send_email
import geclass.user_db
import geclass.course_db


def SendReminder(course_information, survey_type):
    user_db = geclass.user_db.UserDB()
    recipient = user_db.get_email(course_information['user_id'])
    message = """Gute Tag,
    heute beginnt die GEclass {}-Befragung für Ihren Kurs {}. Die Befragung
    kann in den nächsten 10 Tagen abgeschlossen werden. Für die Teilnahme
    benötigen die Studenten die folgenden zwei Informationen:
    Kurs-ID : {}
    URL: https://survey.uni-potsdam.de/s/c21d6139/de.html

    Vielen Dank für die Teilnahme an diesem Projekt!""".format(
        survey_type, course_information['name'],
        course_information['identifier'])
    geclass.send_email.SendEmail(recipient, "Erinnerung GEclass", message)


def FindSurveysStartingToday():
    course_db = geclass.course_db.CourseDB()
    pre, post = course_db.get_surveys_today()
    return pre, post


def SendAllReminders():
    pre, post = FindSurveysStartingToday()
    for row in pre:
        SendReminder(row, "Prä")
    for row in post:
        SendReminder(row, "Post")


@click.command('send-reminder')
@with_appcontext
def ReminderCommand():
    SendAllReminders()


def init_app(app):
    """Create connection to the factory."""
    app.cli.add_command(ReminderCommand)
