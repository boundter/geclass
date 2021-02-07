import click
from flask.cli import with_appcontext
import pandas as pd

from geclass.course_db import CourseDB
from geclass.util.questionnaire_db import QuestionnaireDB


@click.command('get_unmatched')
@with_appcontext
def get_unmatched_students():
    """Get all valid unmatched responses, sorted by course."""
    course_db = CourseDB()
    course_data = list(course_db.get_all_course_data())
    questionnaire_db = QuestionnaireDB()
    data = pd.DataFrame(columns=["course_id", "pre", "post"])
    for course in course_data:
        course_id = course["id"]

        def get_unmatched(pre_post, course_id):
            other = "post" if pre_post == "pre" else "pre"
            res = questionnaire_db.execute("""
                    SELECT
                        student.code
                    FROM
                        student, student_{0}, student_course
                    WHERE
                        student_{0}.student_id = student_course.student_id
                    AND
                        student_course.course_id = ?
                    AND
                        student_{0}.valid_control = 1
                    AND
                        student_{0}.valid_time = 1
                    AND
                        student.id = student_{0}.student_id
                    AND student_{0}.student_id NOT IN (
                        SELECT
                            student_id
                        FROM student_{1}
                    )
                """.format(pre_post, other),
                (course_id,)
            )
            return res

        pre = get_unmatched("pre", course_id)
        for row in pre:
            data = data.append(
                    {"course_id": course_id, "pre": row[0], "post": ""},
                    ignore_index=True
            )
        post = get_unmatched("post", course_id)
        for row in post:
            data = data.append(
                {"course_id": course_id, "pre": "", "post": row[0]},
                ignore_index=True
            )

    data.to_csv("/app/instance/unmatched.csv", index=False)


@click.command('get_unknown_courses')
@with_appcontext
def get_unknown_courses():
    course_db = CourseDB()
    course_data = list(course_db.get_all_course_data())
    data = pd.DataFrame(columns=["known_courses", "unknown_courses"])
    for course in course_data:
        data = data.append(
            {"known_courses": course["identifier"], "unknwon_courses": ""},
            ignore_index=True
        )
    questionnaire_db = QuestionnaireDB()
    res = questionnaire_db.execute(
        "SELECT course_code FROM student_unknown_course",
        ()
    )
    for row in res:
        if row[0] is not None and row[0].strip() != "":
            data = data.append(
                {"known_courses": "", "unknwon_courses": row[0]},
                ignore_index=True
            )
    data.to_csv("/app/instance/unknown.csv", index=False)


def init_app(app):
    app.cli.add_command(get_unmatched_students)
    app.cli.add_command(get_unknown_courses)
