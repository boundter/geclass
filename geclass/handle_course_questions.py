from datetime import date

from geclass.course_question import (
    QuestionText, QuestionDate, QuestionDropdown, QuestionDropdownWithText,
    QuestionNumber, QuestionNote)
from geclass.course_db import CourseDB


class HandleCourseQuestions:
    """Handler for the questions about a new course.

    The member self.question contains all CourseQuestion objects.

    """

    def __init__(self):
        self.db = CourseDB()
        self.values = {}
        self.questions = [
            QuestionText(
                'name', 'Name', 'Wählen Sie einen Namen für den Kurs aus.'),
            QuestionDate(
                'start_date_pre', 'Start Pre-Befragung',
                'Start der Befragung vor dem Kurs. ' +
                'Safari-Nutzer: Bitte in der Form 2019-03-16 angeben.'),
            QuestionDate(
                'start_date_post', 'Start Post-Befragung',
                'Start der Befragung nach dem Kurs. ' +
                'Safari-Nutzer: Bitte in der Form 2019-03-16 angeben.'),
            QuestionDropdownWithText(
                'university', 'Einrichtung',
                'An welcher Einrichtung findet der Kurs statt?',
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
                'traditional', 'Traditionell',
                'Ist der Kurs traditionell?',
                self.db.select_all_entries('traditional')),
            QuestionDropdown(
                'focus', 'Schwerpunkt',
                'Worauf liegt der Schwerpunkt des Kurses?',
                self.db.select_all_entries('focus')),
            QuestionNumber(
                'number_students', 'Anzahl an Studenten',
                ('Wieviele Studenten werden vorraussichtlich an dem Kurs ' +
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
                'Wie ist das Verhältnis von Praktikum zu Vorlesung?',
                default=0, value_range=(0, 1), step=0.1),
            QuestionDropdownWithText(
                'equipment', 'Geräte',
                'Was für eine Art von Geräten wird hauptsächlich verwendet?',
                self.db.select_all_entries('equipment'), 'Andere'),
            QuestionNote(
                'notes', 'Notizen',
                ('Gibt es noch etwas, dass Sie uns sagen wollen? ' +
                 'Max. 255 Zeichen.'))
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
            errors.append('Das Anfangsdatum muss in der Zukunft liegen.')
        # post is after pre
        if not self.values['start_date_pre'] < self.values['start_date_post']:
            errors.append('Start Post-Befragung muss nach der Pre-Befragung sein.')
        return errors

    def write(self, user_id):
        """Write the parsed values to the database.

        Args:
            user_id (str): The id of the owner of the new course.
        """
        self.db.add_course(user_id, self.values)
