class CourseQuestion:

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

    def _input(self):
        inp = '<input name="{}" type="text" value="" required>\n'.format(
            self.name)
        return inp


class QuestionNumber(CourseQuestion):

    def __init__(self, name, title, text, default=None, value_range=None, step=None):
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

    def __init__(self, name, title, text, id_value_pairs):
        self.pairs = id_value_pairs
        super(QuestionDropdown, self).__init__(name, title, text)

    def _input(self):
        options = ''
        for values in self.pairs:
            options += '<option value={}>{}</option>\n'.format(*values)
        inp = '<select name="{}" onchange="{}.submit()"\n'.format(self.name,
                self.name) + options + '</select>\n'
        return inp


class QuestionDropdownWithText(QuestionDropdown):

    def __init__(self, name, title, text, id_value_pairs, other_text):
        self.other_text = other_text
        super(QuestionDropdownWithText, self).__init__(
            name, title, text, id_value_pairs)

    def _input(self):
        dropdown = super(QuestionDropdownWithText, self)._input()
        label = '<label for="{}_free" style="display: inline">{}</label>\n'.format(
            self.name, self.other_text)
        text = '<input name="{}_free" type="text" value="">\n'.format(
            self.name)
        inp = dropdown + '</br>' + label + text
        return inp
