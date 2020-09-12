import sqlite3
import time

import click
from flask import current_app, g
from flask.cli import with_appcontext
import numpy as np

from geclass.db import DBConnection
from geclass.course_db import CourseDB
from geclass.util.responses import Responses, QuestionnaireResponses


class QuestionnaireDB(DBConnection):

    def __init__(self):
        if "questionnaire_db" not in g:
            g.questionnaire_db = sqlite3.connect(
                database=current_app.config["QUESTIONNAIRE_DB"],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.questionnaire_db.row_factory = sqlite3.Row
        self.db = g.questionnaire_db

    def insert_data(self, df):
        course_db = CourseDB()
        for _, row in df.iterrows():
            course_id = course_db.get_course_id(row["course_id"])
            if len(course_id) == 1:
                student_id = self._add_student(row["personal_code"], course_id[0])
            else:
                student_id = self._add_student(row["personal_code"])
                self._add_student_unknown_course(student_id, row["course_id"])
            if row["pre_post"] == 1:
                questionnaire_id = self._add_pre_questionnaire(row)
                self._add_student_prepost(row, student_id, questionnaire_id, "pre")
            elif row["pre_post"] == 2:
                questionnaire_id = self._add_post_questionnaire(row)
                self._add_student_prepost(row, student_id, questionnaire_id, "post")

    def get_matched_responses(self, course_id):
        # TODO: Test
        sql_select_students = """
            SELECT student_id
            FROM student_course
            WHERE course_id = ?"""
        students = self.execute(sql_select_students, (course_id,)).fetchall()
        sql_matched_questionnaires = """
            SELECT
                student_pre.questionnaire_pre_id,
                student_post.questionnaire_post_id
            FROM
                student_pre, student_post
            WHERE
                student_pre.student_id = ?
            AND student_pre.valid_control = 1
            AND student_pre.valid_time = 1
            AND student_post.student_id = ?
            AND student_post.valid_control = 1
            AND student_post.valid_time = 1
            GROUP BY
                student_pre.student_id, student_post.student_id
            HAVING
                COUNT(*) = 1"""
        matched_questionnaires = []
        for student in students:
            print('student:', student[0])
            res = self.execute(
                    sql_matched_questionnaires, (student[0],)*2).fetchone()
            if res is None:
                continue
            matched_questionnaires.append(res)

        def get_questionnaire_result(questionnaire_id, you_expert_mark,
                                     pre_post):
            sql_questionnaire = """
                SELECT *
                FROM questionnaire_{0:}, questionnaire_{1:}
                WHERE
                    questionnaire_{1:}.id = ?
                AND questionnaire_{0:}.id = questionnaire_{1:}.questionnaire_{0:}_id
            """
            q = self.execute(
                    sql_questionnaire.format(you_expert_mark, pre_post),
                    (questionnaire_id,)).fetchone()
            return np.array(
                    [i if i is not None else -998 for i in q[1:]],
                    dtype=np.int16)

        results = []
        for questionnaire in matched_questionnaires:
            print(questionnaire, course_id, matched_questionnaires)
            q_you_pre = get_questionnaire_result(
                    questionnaire[0], "you", "pre")
            q_expert_pre = get_questionnaire_result(
                    questionnaire[0], "expert", "pre")
            q_you_post = get_questionnaire_result(
                    questionnaire[1], "you", "post")
            q_expert_post = get_questionnaire_result(
                    questionnaire[1], "expert", "post")
            q_mark = get_questionnaire_result(
                    questionnaire[1], "mark", "post")
            print(q_you_pre, q_expert_pre, q_you_post, q_expert_post, q_mark)
            results.append(Responses(q_you_pre, q_you_post, q_expert_pre, q_expert_post, q_mark))
        return QuestionnaireResponses(results)

    def get_course_numbers(self, course_id):
        # TODO: Test
        sql_pre = """
            SELECT
                COUNT(student_pre.id),
            FROM student_pre, student_course
            WHERE
                student_course.course_id = ?
            AND student_pre.student_id = student_course.student_id"""
        count_pre = self.execute(sql_pre, (course_id,)).fectchone()[0]
        sql_post = """
            SELECT
                COUNT(student_post.id),
            FROM student_post, student_course
            WHERE
                student_course.course_id = ?
            AND student_post.student_id = student_course.student_id"""
        count_post = self.execute(sql_post, (course_id,)).fectchone()[0]
        return count_pre, count_post


    def _add_student(self, code, course_id=None):
        if course_id == None:
            return self.add_and_get_id('student', ('code',), (code,))
        sql = """
            SELECT student.id
            FROM student, student_course
            WHERE
                student_course.course_id = ?
            AND student.id = student_course.student_id
            AND student.code = ?"""
        rows = self.execute(sql, (course_id, code)).fetchall()
        if len(rows) == 1:
            return rows[0][0]
        student_id = self.add_and_get_id('student', ('code',), (code,))
        self._add_student_course(student_id, course_id)
        return student_id

    def _add_student_course(self, student_id, course_id):
        columns = ["student_id", "course_id"]
        values = [student_id, course_id]
        self.add(table="student_course", columns=columns, values=values)

    def _add_student_unknown_course(self, student_id, course_code):
        columns = ["student_id", "course_code"]
        values = [student_id, course_code]
        self.add(table="student_unknown_course", columns=columns,
                 values=values)

    def _add_questionnaire(self, row, you_expert):
        columns = ["q{:d}".format(i) for i in range(1, 31)]
        values = [
                row["q{:d}_{:d}".format(i, 1 if you_expert == "you" else 2)]
                for i in range(1, 31)
        ]
        last_id = self.add_and_get_id("questionnaire_{}".format(you_expert),
                                      columns=columns, values=values)
        return last_id

    def _add_questionnaire_mark(self, row):
        columns = ["q{:d}".format(i) for i in range(1, 24)]
        values = [row["post_{:d}".format(i)] for i in range(1, 24)]
        last_id = self.add_and_get_id("questionnaire_mark",
                                      columns=columns, values=values)
        return last_id

    def _add_pre_questionnaire(self, row):
        columns = ["questionnaire_you_id", "questionnaire_expert_id"]
        you_id = self._add_questionnaire(row, "you")
        expert_id = self._add_questionnaire(row, "expert")
        values = [you_id, expert_id]
        last_id = self.add_and_get_id("questionnaire_pre", columns=columns,
                values=values)
        return last_id

    def _add_post_questionnaire(self, row):
        columns = ["questionnaire_you_id", "questionnaire_expert_id",
                "questionnaire_mark_id"]
        you_id = self._add_questionnaire(row, "you")
        expert_id = self._add_questionnaire(row, "expert")
        mark_id = self._add_questionnaire_mark(row)
        values = [you_id, expert_id, mark_id]
        last_id = self.add_and_get_id("questionnaire_post", columns=columns,
                values=values)
        return last_id

    def _add_student_prepost(self, row, student_id, questionnaire_id, pre_post):
        start = int(time.mktime(row["start"].timetuple()))
        end = int(time.mktime(row["end"].timetuple()))
        columns = ["student_id", "questionnaire_{}_id".format(pre_post), "start_time", "end_time", "valid_control", "valid_time"]
        values = [student_id, questionnaire_id, start, end, int(row["valid_control"]), int(row["valid_time"])]
        self.add("student_{}".format(pre_post), columns=columns, values=values)


def init_questionnaire_db():
    db = QuestionnaireDB()
    with current_app.open_resource('util/schema_questionnaire.sql') as f:
        db().executescript(f.read().decode('utf8'))


@click.command('init-questionnaire-db')
@with_appcontext
def init_questionnaire_db_command():
    """Create CLI for creating a new database with `flask init-db`.

    **Careful: This will overwite the current one and all data will
    be lost.**

    """
    init_questionnaire_db()
    click.echo('Initialized the questionnaire database')


def close_questionnaire_db(e=None):
    """Close the database. Needed for the teardown."""
    db = g.pop(name='questionnaire_db', default=None)
    if db is not None:
        db.close()


def init_app(app):
    """Create connection to the factory."""
    app.teardown_appcontext(close_questionnaire_db)
    app.cli.add_command(init_questionnaire_db_command)
