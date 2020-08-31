"""A class to handle the course management."""
from datetime import date
import logging
import secrets
import string
import time

from geclass.db import DBConnection
from geclass.user_db import UserDB
import geclass.send_email

log = logging.getLogger(__name__)


class CourseDB(DBConnection):
    """Handle the course  management."""

    def get_courses(self, user_id):
        """Fetch all coursed from user with given id.

        Args:
            user_id (int): The id of the owner of the courses.

        Returns:
            A list of all the sqlite3 rows of the courses.

        >>> courses = get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['course_identifier'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'

        """
        return self.select_all(table='course', column='user_id', value=user_id)

    def add_course(self, user_id, fields):
        """Add a new course to the database.

        Args:
            user_id (int): The id of the owner of the course.
            course_name (str): Some name for the course. It
                               does not need to be unique.

        >>> get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['name'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'
        >>> add_course(user_id=1, name='a_new_name')
        >>> get_courses(user_id=1)
        >>> for course in courses:
        ...     print(course['name'])
        'uni_potsdam_biochem_2018'
        'uni_potsdam_phys_2018'
        'a_new_name'

        """
        log.info('Added new course %s for user %s', fields['name'], user_id)
        columns = ['user_id', 'identifier']
        values = [str(user_id), self.generate_identifier()]
        for key in fields:
            columns.append(key)
            values.append(fields[key])
        course_name = fields["name"]
        pre_start_date = fields["start_date_pre"]
        pre_start_date = date.fromtimestamp(int(fields['start_date_pre']))
        user_db = UserDB()
        email = user_db.get_email(user_id)
        geclass.send_email.SendEmail(
            email,
            'Kurs Registrierung GEclass',
            """Vielen Dank, dass Sie den Kurs {} bei der  GEclass registriert haben.
Die ID des Kurses lautet: {}.
Die Prä-Befragung startet am {}. Sie werden an diesem Tag auch eine Erinnerungsemail erhalten.

Vielen Dank für die Teilnahme an diesem Projekt.""".format(
                course_name, values[1], pre_start_date.isoformat()),
        )
        self.add(
            table='course',
            columns=columns,
            values=values)


    def generate_identifier(self):
        """Generate a random unique identifier of length 5 and return it."""
        length = 5
        sql = 'SELECT identifier FROM course'
        ids = self.execute(sql, ()).fetchall()
        if len(ids) == 0:
            ids.append('0'*length)
        key = ids[0]
        ids = set(ids)
        while key in ids:
            key = ''.join(
                secrets.choice(string.ascii_lowercase) for _ in range(length))
        return key

    def get_surveys_today(self):
        """Return pre and post surveys that start today."""
        date_today = date.today()
        timestamp_today = str(int(time.mktime(date_today.timetuple())))
        sql_pre = """
            SELECT
                user_id,
                name,
                identifier
            FROM course
            WHERE course.start_date_pre = ?"""
        sql_post = """
            SELECT
                user_id,
                name,
                identifier
            FROM course
            WHERE course.start_date_post = ?"""
        pre_surveys = self.execute(sql_pre, (timestamp_today,)).fetchall()
        post_surveys = self.execute(sql_post, (timestamp_today,)).fetchall()
        return pre_surveys, post_surveys

    def get_course_id(self, identifier):
        # TODO: Test
        sql = "SELECT id FROM course WHERE identifier = ?"
        return self.execute(sql, (identifier,)).fetchall()

    def get_overview(self, user_id):
        sql = """
            SELECT
              course.identifier,
              course.name,
              university.university_name,
              program.program_name,
              experience.experience_level,
              number_students,
              strftime('%d.%m.%Y', start_date_pre, 'unixepoch'),
              strftime('%d.%m.%Y', start_date_post, 'unixepoch')
            FROM course, university, program, experience
            WHERE course.user_id = ?
              AND university.id = course.university_id
              AND program.id = course.program_id
              AND experience.id = course.experience_id"""
        return self.execute(sql, (user_id,)).fetchall()

    def get_course_questionnaire_dates(self, course_identifier):
        sql = """
            SELECT
              start_date_pre
              start_date_post
            FROM course
            WHERE course.identifier = ?"""
        times = self.execute(sql, (course_identifier,)).fetchall()
        if len(times) != 1:
            return None
        return {"pre": times[0][0], "post": times[0][1]}

    def _add_and_get_new_id(self, table, column, value):
        """Add a new entry to the given table.

        Careful: `table` and `column`are not sqnitized.

        """
        log.info('Add new value %s to table %s', value, table)
        self.add(table, (column,), (value,))
        new_entry = self.select_one(table, column, value)
        return new_entry['id']

    def add_and_get_id_university(self, value):
        """Add a new entry to the university table and get its id.

        Args:
            value (str): The new value to add to the table.

        >>> add_and_get_id_university("Uni München")
        3

        """
        return self._add_and_get_new_id('university', 'university_name', value)

    def add_and_get_id_equipment(self, value):
        """Add a new entry to the equipment table and get its id.

        Args:
            value (str): The new value to add to the table.

        >>> add_and_get_id_equipment("Leitz")
        3

        """
        return self._add_and_get_new_id('equipment', 'equipment_type', value)

    def add_and_get_id_note(self, value):
        """Add a new entry to the notes table and get its id.

        Args:
            value (str): The new value to add to the table.

        >>> add_and_get_id_note("This is a new note")
        3

        """
        return self._add_and_get_new_id('notes', 'notes_text', value)
