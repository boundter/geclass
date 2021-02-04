import click
from flask.cli import with_appcontext

from geclass.course_db import CourseDB
from geclass.util.questionnaire_db import QuestionnaireDB


@click.command('validate_time')
@click.argument('pre_post')
@click.argument('course_name')
@with_appcontext
def validate_all(pre_post, course_name):
    """Set the time validity for all students of a course to 1."""
    course_db = CourseDB()
    course_id = course_db.get_course_id(course_name)[0]
    questionnaire_db = QuestionnaireDB()
    if pre_post not in ["pre", "post"]:
        print("Unknown pre_post specifier {}, should be 'pre' or 'post'"
              "".format(pre_post))
        return
    query =  """
    UPDATE
        student_{}
    SET
        valid_time = 1
    WHERE student_id IN (
        SELECT
            student_id
        FROM
            student_course
        WHERE
            course_id = ?
    )
    """.format(pre_post)
    questionnaire_db.execute(query, (course_id,))
    questionnaire_db.db.commit()


def init_app(app):
    app.cli.add_command(validate_all)
