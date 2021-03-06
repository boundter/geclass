"""Container to generate html-expressions for adding courses."""

import time
import re
from datetime import date

from geclass.course_db import CourseDB

class StartTab:
    """Start a new tab in the questionnaire."""

    def __repr__(self):
        return '<div class="tab">\n'

    def parse(self, form):
        return None


class EndTab:
    """End the current tab in the questionnaire."""

    def __repr__(self):
        return '</div>\n'

    def parse(self, form):
        return None


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

        >>> parse(form) # for the field "name"
        ("name", "a new course name")

        """
        if not form[self.name]:
            raise KeyError('Feld {} wird benötigt.'.format(self.title))
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


class QuestionFrequency():
    """Create multiple questions with four radio buttons.

    Args:
        fields (dicy(str, str)): A dict consisting of the id of the
                                 field and its text.
        title (str): The title of the questions.

    """

    def __init__(self, fields, title):
        self.fields = fields
        self.title = title

    def __repr__(self):
        div_begin = '<div class="course_question">\n'
        header = '<h3>{}</h3>\n'.format(self.title)
        question = []
        for n, t in self.fields.items():
            question.append(
                    '''<tr>
                        <td>{}</td>
                        <td><input type="radio" name="{}" value="3" required></td>
                        <td><input type="radio" name="{}" value="2"></td>
                        <td><input type="radio" name="{}" value="1"></td>
                        <td><input type="radio" name="{}" value="0"></td>
                       </tr>\n'''.format(t, n, n, n, n))
        table = '''<table>
            <tr>
                <th></th>
                <th>Immer</th>
                <th>Oft</th>
                <th>Selten</th>
                <th>Nie</th>
            </tr>\n'''
        for q in question:
            table += q
        table += '</table>\n'
        div_end = '</div>\n'
        html = div_begin + header + table + div_end
        return html

    def parse(self, form):
        keys = []
        for name in self.fields:
            if not form[name]:
                raise KeyError('Feld {} wird benötigt.'.format(self.fields[name]))
            else:
                keys.append((name, form[name]))
        return keys




class QuestionNote(QuestionText):
    """Create a question with a note field.

    Args:
        name (str): The html identifier for the input.
        title (str): The header of the question.
        text (str): The label of the input, it acts as an
            explanation.
    """

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
            raise KeyError('Feld {} wird benötigt.'.format(self.title))
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
            raise KeyError('Feld {} wird benötigt.'.format(self.title))
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
            StartTab(),
            QuestionText(
                'name', 'Name', 'Wählen Sie einen beliebigen Namen für den Kurs aus.'),
            QuestionDate(
                'start_date_pre', 'Start Prä-Befragung',
                'Start der Befragung vor dem Kurs. Die Befragung ist 14 Tage aktiv.' +
                'Safari-Nutzer: Bitte in der Form 2019-03-16 angeben.'),
            QuestionDate(
                'start_date_post', 'Start Post-Befragung',
                'Start der Befragung nach dem Kurs. Die Befragung ist 14 Tage aktiv.' +
                'Safari-Nutzer: Bitte in der Form 2019-03-16 angeben.'),
            QuestionDropdown(
                'university_type', 'Art der Hochschule',
                'An welcher Art von Hochschule findet der Kurs statt?',
                self.db.select_all_entries('university_type')),
            QuestionDropdownWithText(
                'university', 'Hochschule',
                'An welcher Hochschule findet der Kurs statt?',
                self.db.select_all_entries('university'), 'Andere'),
            QuestionDropdown(
                'program', 'Studiengang',
                'Zu welchen Studiengang gehört der Kurs?',
                self.db.select_all_entries('program')),
            QuestionDropdown(
                'experience', 'Jahrgang',
                'In welchem Jahrgang sind die Studenten?',
                self.db.select_all_entries('experience')),
            QuestionDropdown(
                'course_type', 'Art des Kurses',
                'Was für eine Art von Kurs ist es?',
                self.db.select_all_entries('course_type')),
            QuestionDropdown(
                'traditional', 'Didaktische Methoden',
                'Welche didaktischen Methoden benutzt der Kurs?',
                self.db.select_all_entries('traditional')),
            QuestionDropdown(
                'focus', 'Schwerpunkt',
                'Worauf liegt der Schwerpunkt des Kurses?',
                self.db.select_all_entries('focus')),
            QuestionNumber(
                'number_students', 'Anzahl an Studenten',
                ('Wieviele Studenten werden voraussichtlich an dem Kurs ' +
                 'teilnehmen?'), default=0, value_range=(0, 1000)),
            QuestionNumber(
                'students_per_instructor', 'Verhältnis Studenten/Betreuer',
                'Wieviele Studenten kommen in etwa auf einen Betreuer?',
                default=0, value_range=(0, 100)),
            QuestionNumber(
                'number_experiments', 'Nummer von Experimenten',
                'Wieviele Experimente muss jeder Student durchführen?',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'number_projects', 'Nummer von Projekten',
                'Wieviele Projekte muss jeder Student durchführen?',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'lab_per_lecture', 'Verhältnis Praktikum/Vorlesung',
                'Wie ist das Verhältnis von Praktikum zu Vorlesung? (Angabe als z.B. 0.5)',
                default=0, value_range=(0, 100), step=0.1),
            QuestionNumber(
                'hours_per_lab', 'Länge eines Termins',
                'Wieviele Stunden dauert ein Termin?',
                default=0, value_range=(0, 24), step=0.01),
            QuestionNumber(
                'number_labs', 'Anzahl Termine',
                'Wieviele Termine gibt es?',
                default=0, value_range=(0, 1000)),
            QuestionNumber(
                'week_guided', 'Geführte Wochen',
                'Wieviel Wochen sind die Experiment geführt?',
                default=0, value_range=(0, 1000)),
            QuestionDropdownWithText(
                'equipment', 'Geräte',
                'Was für eine Art von Geräten wird hauptsächlich verwendet?',
                self.db.select_all_entries('equipment'), 'Andere'),
            EndTab(),
            StartTab(),
            QuestionFrequency(
                {'frequency_phys_principle': 'bekannte physikalische Prinzipien verifizieren?',
                 'frequency_known_principle': 'bekannte physikalische Prinzipien durch selbstständiges Experimentieren wiederentdecken?',
                 'frequency_unknown_principle': 'offene Fragen untersuchen, deren Antwort unbekannt ist?'},
                'Wie oft werden Studenten in dem Praktikum ...'),
            QuestionFrequency(
                {'students_questions': 'der eigenen Fragestellung?',
                 'students_plan': 'der Planung der Messmethode?',
                 'students_design': 'dem Design des Messaubaus?',
                 'students_apparatus': 'dem Aufbau der Messapparate?',
                 'students_analysis': 'der selbstständigen Ausarbeitung der Auswertung?',
                 'students_troubleshoot': 'dem Troubleshooting des Messapparates?',
                 'students_groups': 'der Gruppenarbeit?'},
                'Wie oft arbeiten Studenten an ...'),
            QuestionFrequency(
                {'modeling_mathematics': 'die mathematische Modellierung des physikalischen Systems',
                 'modeling_model': 'die konzeptuelle Modellierung des physikalischen Systems',
                 'modeling_tools': 'Modellierung des physikalischen Aufbau',
                 'modeling_measurement': 'Modellierung der Messgeräte',
                 'modeling_predictions': 'Angabe von Vorhersagen, die durch mathematische oder physikalische Modelle entstehen',
                 'modeling_uncertainty': 'um das Messsystem order die Messprozedur zu verbessern und die Messunsicherheiten zu reduzieren',
                 'modeling_calibrate': 'Kalibrierung der Messgeräte'},
                'Studenten modellieren selbstständig durch ...'),
            QuestionFrequency(
                {'analysis_uncertainty': 'der direkten Bestimmung der Messunsicherheiten',
                 'analysis_calculate': 'Bestimmung der Messunsicherheiten durch Fehlerfortpflanzung',
                 'analysis_computer': 'Berechnung/Visualisierung am Computer',
                 'analysis_control': 'Computersteuerung der Messgeräte'},
                'Studenten führen die Auswertung und die Visualisierung der Daten durch mit ...'),
            QuestionFrequency(
                {'communication_oral': 'die Ergebnisse in einer mündlichen Präsentation',
                 'communication_written': 'die Ergebnisse in einer schriftlichen Präsentation/Bericht',
                 'communication_journal': 'die Ergebnisse in Form eines Journalartikels',
                 'communication_lab': 'den Versuchsablauf in einem Laborbuch',
                 'communication_test': 'die Vorbereitung mit einem Testat'},
                'Studenten kommunizieren  ...'),
            QuestionNote(
                'notes', 'Notizen',
                ('Gibt es noch etwas, dass Sie uns sagen wollen? ' +
                 'Max. 255 Zeichen.')),
            EndTab()
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
                    if len(parsed_data) >= 2 and len(parsed_data[0]) == 2:
                        for data in parsed_data:
                            self.values[data[0]] = data[1]
                    else:
                        self.values[parsed_data[0]] = parsed_data[1]
            except Exception as e:
                errors.append(e)
        try:
            errors.extend(self._sanity_check())
        except KeyError as e:
            pass
        return errors

    def _sanity_check(self):
        """Check the sanity of the data.

        1. Check if both start-dates are in the future.
        2. Post is after Pre Date
        3. All frequency questions have int values between 0 and 3
        """
        errors = []
        # all dates in future
        if not (
                (date.fromtimestamp(int(self.values['start_date_pre'])) >
                 date.today()) &
                (date.fromtimestamp(int(self.values['start_date_post'])) >
                 date.today())):
            errors.append('Das Anfangsdatum muss in der Zukunft liegen.')
        # post is after pre
        if not self.values['start_date_pre'] < self.values['start_date_post']:
            errors.append('Start Post-Befragung muss nach der Pre-Befragung sein.')
        frequency_questions = [
                'frequency_*', 'students_*^(?!_)', 'modeling_*', 'analysis_*',
                'communication_*']
        for key in self.values:
            if any(re.match(expr, key) for expr in frequency_questions):
                if not (int(self.values[key]) in [0, 1, 2, 3]):
                    errors.append('Flascher Wert im Feld {}'.format(key))
        return errors

    def write(self, user_id):
        """Write the parsed values to the database.

        Args:
            user_id (str): The id of the owner of the new course.
        """
        self.db.add_course(user_id, self.values)
