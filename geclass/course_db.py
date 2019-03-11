import logging

from geclass.db import DBConnection

log = logging.getLogger(__name__)


class CourseDB(DBConnection):

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
        return self.select_all(table='course', field='user_id', value=user_id)

    def add_course(self, user_id, course_name):
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
        log.info(
            'Added new course {} for user {}'
            ''.format(course_name, user_id))
        self.add(
            table='course',
            field=('user_id', 'name'),
            values=(user_id, course_name))
