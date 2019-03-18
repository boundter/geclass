"""Container to generate html-expressions for adding courses."""

import time
from datetime import date

from geclass.course_db import CourseDB


class CourseQuestion:
    """Base class of the questions.

    All questions should inherit from CourseQuestions. The
    html-expression can be accessed by calling __repr__. Children
    need to implement the _input(self) function to generate the
    specific html for the type of question, as well as the parse method.

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

    def parse(self, form):
        """Parse the form to find the corresponfing value from the form.

        Args:
            form (dict(str: str)): The form returned from the webpage.

        Returns:
            A tuple of the name of the column in the table course as
            well as its value.

        >>> parse(form) // for the field "name"
        ("name", "a new course name")

        """
        if not form[self.name]:
            raise KeyError('{} is required.'.format(self.title))
        else:
            return (self.name, form[self.name])


class QuestionText(CourseQuestion):
    """Create a question with a free text field.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
        max_length (int): The max length of the input.

    """

    def __init__(self, name, title, text, max_length=255):
        self.max_length = max_length
        super(QuestionText, self).__init__(name, title, text)

    def _input(self):
        if self.max_length:
            length = ' maxlength="{}"'.format(self.max_length)
        else:
            length = ''
        inp = '<input name="{}" type="text" value="" {}required>\n'.format(
            self.name, length)
        return inp


class QuestionNote(QuestionText):

    def _input(self):
        inp = ('<textarea rows="5" cols="51" name="{}" onchange="{}.submit()">'
               ''.format(self.name, self.name) + '</textarea>')
        return inp

    def parse(self, form):
        if form[self.name]:
            db = CourseDB()
            new_id = db.add_and_get_id_note(form[self.name])
            return (self.name + '_id', new_id)
        return None


class QuestionDate(CourseQuestion):
    """Create a question with a date.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
    """

    def _input(self):
        inp = '<input name="{}" type="date" value=""required>\n'.format(
            self.name)
        return inp

    def parse(self, form):
        if not form[self.name]:
            raise KeyError('{} is required.'.format(self.title))
        else:
            day = date(*map(int, form[self.name].split('-')))
            timestamp = str(int(time.mktime(day.timetuple())))
            return (self.name, timestamp)


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

    def parse(self, form):
        if not form[self.name]:
            raise KeyError('{} is required.'.format(self.title))
        else:
            return (self.name + '_id', form[self.name])


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

    def parse(self, form):
        free_text = form[self.name + '_free'].strip()
        if not free_text:
            return super(QuestionDropdownWithText, self).parse(form)
        db = CourseDB()
        add_new_value = {
            'university': db.add_and_get_id_university,
            'equipment': db.add_and_get_id_equipment}
        new_id = add_new_value[self.name](free_text)
        return (self.name + '_id', new_id)


class HandleCourseQuestions:
    """Handler for the questions about a new course.

    The member self.question contains all CourseQuestion objects.

    """

    def __init__(self):
        self.db = CourseDB()
        self.values = {}
        self.questions = [
            QuestionText('name', 'Name', 'Choose a name for your course.'),
            QuestionDate(
                'start_date_pre', 'Start Date Pre',
                'The start date of the first questionaire. ' +
                'Dates should be in the form 2019-03-16 for Safari users.'),
            QuestionDate(
                'start_date_post', 'Start Date Post',
                'The start date of the second questionaire.' +
                'Dates should be in the form 2019-03-16 for Safri users.'),
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
                ('How many students are going to be in the course? ' +
                 '(Approximately)'), default=0, value_range=(0, 1000)),
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
            QuestionNote(
                'notes', 'Notes',
                ('Is there anything else, you want to tell us? ' +
                 'Max 255 characters.'))
        ]

    def __iter__(self):
        for question in self.questions:
            yield question

    def parse(self, form):
        """Parse a given form for the values for the new course.

        Args:
            form (dict(str: str)): The form returned from the webpage.

        Returns:
            A list of all the errors it encountered while parsing.

        >>> parse({"name": ""})
        ["Name is required."]

        """
        errors = []
        for question in self.questions:
            try:
                parsed_data = question.parse(form)
                if parsed_data:
                    self.values[parsed_data[0]] = parsed_data[1]
            except KeyError as e:
                errors.append(e)
        try:
            errors.extend(self._sanity_check())
        except KeyError as e:
            pass
        return errors

    def _sanity_check(self):
        errors = []
        # all dates in future
        if not (
                (date.fromtimestamp(int(self.values['start_date_pre'])) >
                 date.today()) &
                (date.fromtimestamp(int(self.values['start_date_post'])) >
                 date.today())):
            errors.append('Start dates must be in the future.')
        # post is after pre
        if not self.values['start_date_pre'] < self.values['start_date_post']:
            errors.append('Start date post must be after start date pre.')
        return errors

    def write(self, user_id):
        """Write the parsed values to the database.

        Args:
            user_id (str): The id of the owner of the new course.
        """
        self.db.add_course(user_id, self.values)
