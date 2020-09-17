"""Utilities to send out a reminder for upcoming questionnaires.

The reminders can be send out with the command

    $ flask send-reminder

All persons with questionnaires starting today will be informed.

"""

import click
from flask.cli import with_appcontext

import geclass.course_db
import geclass.send_email
import geclass.user_db


def SendReminder(course_information, survey_type):
    """Send out a reminder for a given course.

    Args:
        course_information (sqlite3.Row): The information of the course
            containing the user_id, the name and the identifier.
        survey_type (str): Either 'Prä' or 'Post'. Is only used for the text.

    """
    user_db = geclass.user_db.UserDB()
    recipient = user_db.get_email(course_information['user_id'])
    message = '''Gute Tag,
heute beginnt die GEclass {}-Befragung für Ihren Kurs {}. Die Befragung
kann in den nächsten 14 Tagen abgeschlossen werden. Für die Teilnahme
benötigen die Studenten die folgenden zwei Informationen:
Kurs-ID : {}
URL: https://survey.uni-potsdam.de/s/c21d6139/de.html

Vielen Dank für die Teilnahme an diesem Projekt!'''.format(
        survey_type, course_information['name'],
        course_information['identifier'])
    geclass.send_email.SendEmail(recipient, 'Erinnerung GEclass', message)


def SendOverview(pre, post):
    """Send out an overview of all questionnaires today to ge-class@up.

    Args:
        pre (list): A list containing all pre courses for today (only len is
            used).
        post (list): A list containing all post courses for today (only len
            is used).

    """
    recipient = 'ge-class@uni-potsdam.de'
    subject = 'GEclass: Täglicher Report'
    message = '''Heute finden {} Prä- und {} Post-Surveys statt.'''.format(
            len(pre), len(post))
    geclass.send_email.SendEmail(recipient, subject, message)


def FindSurveysStartingToday():
    """Get all Surveys that start today.

    Returns:
        (pre, post) where pre and post are a list of sqlite3.Rows containing
            information about the courses.
    """
    course_db = geclass.course_db.CourseDB()
    pre, post = course_db.get_surveys_today()
    return pre, post


def SendAllReminders():
    """Send out all the reminders for today's courses."""
    pre, post = FindSurveysStartingToday()
    for row in pre:
        SendReminder(row, 'Prä')
    for row in post:
        SendReminder(row, 'Post')
    SendOverview(pre, post)



@click.command('send-reminder')
@with_appcontext
def ReminderCommand():
    SendAllReminders()


def init_app(app):
    """Create connection to the factory."""
    app.cli.add_command(ReminderCommand)
