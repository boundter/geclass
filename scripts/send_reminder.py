import sys
sys.path.append("..")

import geclass.send_email
from geclass.user_db import UserDB
from geclass.course_db import CourseDB


def SendReminder(course_information, survey_type):
    user_db = UserDB()
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


def FindSurveysStartingToday()
    course_db = CourseDB()
    pre, post = course_db.get_surveys_today()
    return pre, post


def main():
    pre, post = FindSurveysStartingToday()
    for row in pre:
        SendReminder(row, "Prä")
    for row in post:
        SendReminder(row, "Post")


if __name__ == "__main__":
    main()
