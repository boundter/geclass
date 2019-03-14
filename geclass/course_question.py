"""Container to generate html-expressions for adding courses."""

import time
from datetime import date
import logging

from geclass.course_db import CourseDB

log = logging.getLogger(__name__)


class CourseQuestion:
    """Base class of the questions.

    All questions should inherit from CourseQuestions. The
    html-expression can be accessed by calling __repr__. Children
    need to implement the _input(self) function to generate the
    specific html for the type of question.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.

    """

    def __init__(self, name, title, text):
        self.name = name
        self.title = title
        self.text = text

    def __repr__(self):
        div_begin = '<div class="course_question">\n'
        header = '<h3>{}</h3>\n'.format(self.title)
        label = '<label for="{}">{}</label>\n'.format(self.name, self.text)
        inp = self._input()
        div_end = '</div>\n'

        html = div_begin + header + label + inp + div_end
        return html

    def _input(self):
        return ''


class QuestionText(CourseQuestion):
    """Create a question with a free text field.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
        max_length (int): The max length of the input.
    """

    def __init__(self, name, title, text, max_length=None, required=False):
        self.max_length = max_length
        self.required = required
        super(QuestionText, self).__init__(name, title, text)

    def _input(self):
        if self.max_length:
            length = ' maxlength="{}"'.format(self.max_length)
        else:
            length = ''
        if self.required:
            req = ' required'
        else:
            req = ''
        inp = '<input name="{}" type="text" value=""{}{}>\n'.format(
            self.name, length, req)
        return inp


class QuestionDate(CourseQuestion):
    """Create a question with a date.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
    """

    def __init__(self, name, title, text):
        super(QuestionDate, self).__init__(name, title, text)

    def _input(self):
        inp = '<input name="{}" type="date" value=""required>\n'.format(
            self.name)
        return inp


class QuestionNumber(CourseQuestion):
    """Create a question with a number.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
        default (int or float): The default value of the field.
        value_range (list(int, int)) or (list(float, float)): The
            allowed range of the value.
        step (int or float): Stepszize of the field.
            Gives the precision.

    """

    def __init__(
            self, name, title, text, default=None, value_range=None,
            step=None):
        self.default = default
        self.value_range = value_range
        self.step = step
        super(QuestionNumber, self).__init__(name, title, text)

    def _input(self):
        if self.default is not None:
            value = 'value={} '.format(self.default)
        else:
            value = ''
        if self.value_range:
            val_range = 'min={} max={} '.format(*self.value_range)
        else:
            val_range = ''
        if self.step is not None:
            increment = 'step={} '.format(self.step)
        else:
            increment = ''
        inp = '<input name="{}" type="number" {}{}{}required>\n'.format(
            self.name, value, val_range, increment)
        return inp


class QuestionDropdown(CourseQuestion):
    """Create a question with a dropdown menu.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
        id_value_pairs (list(list(int, str))): The pair of the id of
            the value and a string representing it. Can be
            generated with a statement of the sort
            'SELECT id, field FROM ...'.
    """

    def __init__(self, name, title, text, id_value_pairs):
        self.pairs = id_value_pairs
        super(QuestionDropdown, self).__init__(name, title, text)

    def _input(self):
        options = ''
        for values in self.pairs:
            options += '<option value={}>{}</option>\n'.format(*values)
        inp = ('<select name="{}" onchange="{}.submit()">\n'
               ''.format(self.name, self.name) + options + '</select>\n')
        return inp


class QuestionDropdownWithText(QuestionDropdown):
    """Create a question with a dropdown menu and a free text field.

    The text field has the same html name as the dropbown with _free
    added. So name="test" leads to "test_free".

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
        id_value_pairs (list(list(int, str))): The pair of the id of
            the value and a string representing it. Can be
            generated with a statement of the sort
            'SELECT id, field FROM ...'.
        other_text (str): The label of the free text field.

    """

    def __init__(self, name, title, text, id_value_pairs, other_text):
        self.other_text = other_text
        super(QuestionDropdownWithText, self).__init__(
            name, title, text, id_value_pairs)

    def _input(self):
        dropdown = super(QuestionDropdownWithText, self)._input()
        label = ('<label for="{}_free" style="display: inline">{}</label>\n'
                 ''.format(self.name, self.other_text))
        text = '<input name="{}_free" type="text" value="">\n'.format(
            self.name)
        inp = dropdown + '</br>' + label + text
        return inp


class CreateQuestions:

    def __init__(self):
        self.db = CourseDB()
        self.questions = [
            QuestionText('name', 'Name', 'Choose a name for your course.'),
            QuestionDate(
                'start_date_pre', 'Start Date Pre',
                'The start date of the first questionaire.'),
            QuestionDate(
                'start_date_post', 'Start Date Post',
                'The start date of the second questionaire.'),
            QuestionDropdownWithText(
                'university', 'University', 'Where is the course?',
                self.db.select_all_entries('university'), 'Other'),
            QuestionDropdown(
                'program', 'Program', 'What program are the students in?',
                self.db.select_all_entries('program')),
            QuestionDropdown(
                'experience', 'Experience Level of the Students',
                'How experienced are the students?',
                self.db.select_all_entries('experience')),
            QuestionDropdown(
                'course_type', 'Type of Course',
                'What type of course is it?',
                self.db.select_all_entries('course_type')),
            QuestionDropdown(
                'traditional', 'Traditional',
                'Is the course traditional or non-traditional?',
                self.db.select_all_entries('traditional')),
            QuestionDropdown(
                'focus', 'Focus',
                'What is the focus of the course?',
                self.db.select_all_entries('focus')),
            QuestionNumber(
                'number_students', 'Number of Students',
                'How many students are going to be in the course? (Approximately)',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'students_per_instructor', 'Ratio of Students to Instructors',
                'How many students are there per instructor?', default=0,
                value_range=(0, 100)),
            QuestionNumber(
                'number_experiments', 'Number of Experiments',
                'How many experiments does each student need to complete?',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'number_projects', 'Number of Projects',
                'How many projects does each student need to complete?',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'lab_per_lecture', 'Ratio of Lab to Lecture',
                'What is the ratio of lab to lecture in the course?',
                default=0, value_range=(0, 1), step=0.1),
            QuestionDropdownWithText(
                'equipment', 'Equipment',
                'What type of equipments is mainly used?',
                self.db.select_all_entries('equipment'), 'Other'),
            QuestionText(
                'notes', 'Notes',
                'Is there anything else, you want to tell us? Max 255 characters.',
                max_length=255, required=False)
            ]

    def __iter__(self):
        for question in self.questions:
            yield question


class QuestionParser:

    def __init__(self, form):
        self.db = CourseDB()
        self.form = form
        self.field = {}
        self.errors = []
        self.free_field = {
            'university': self.db.add_and_get_id_university,
            'equipment': self.db.add_and_get_id_equipment}

        self._parse_simple('name', 'Name')
        self._parse_simple('start_date_pre', 'Start Date Pre')
        self._parse_simple('start_date_post', 'Start Date Post')
        self._parse_simple('program', 'Program', id_field=True)
        self._parse_simple('experience', 'Experience Level', id_field=True)
        self._parse_simple('course_type', 'Type of Course', id_field=True)
        self._parse_simple('traditional', 'Traditional', id_field=True)
        self._parse_simple('focus', 'Focus', id_field=True)
        self._parse_simple('number_students', 'Number of Students')
        self._parse_simple('students_per_instructor', 'Ratio of Students to Instructors')
        self._parse_simple('number_experiments', 'Number of Experiments')
        self._parse_simple('number_projects', 'Number of Projects')
        self._parse_simple('lab_per_lecture', 'Ration of Lab to Lecture')
        # parse notes
        self._parse_complex('university', 'University')
        self._parse_complex('equipment', 'Equipment')

    def _parse_simple(self, name, field_name, id_field=False):
        if not self.form[name]:
            self.errors.append('{} is required.'.format(field_name))
        else:
            if id_field:
                self.field[name + '_id'] = self.form[name]
            else:
                self.field[name] = self.form[name]

    def _parse_complex(self, name, field_name):
        free = self.form[name + '_free'].strip()
        if not free:
            self._parse_simple(name, field_name, id_field=True)
        else:
            new_id = self.free_field[name](free)
            self.field[name + '_id'] = new_id

    def write(self, user_id):
        for key in ['start_date_pre', 'start_date_post']:
            day = date(*map(int, self.field[key].split('-')))
            timestamp = str(int(time.mktime(day.timetuple())))
            self.field[key] = timestamp
        log.debug('fields = %s', self.field)
        self.db.add_course(user_id, self.field)





