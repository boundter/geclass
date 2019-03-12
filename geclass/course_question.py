"""Container to generate html-expressions for adding courses."""


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
    """

    def _input(self):
        inp = '<input name="{}" type="text" value="" required>\n'.format(
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
        inp = ('<select name="{}" onchange="{}.submit()"\n'
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
