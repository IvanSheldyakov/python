from datetime import datetime

from wtforms import StringField, validators, Form, DateField


class UniversityForm(Form):
    name = StringField('Полное наименование', [validators.Length(min=1, max=70)])
    short_name = StringField('Сокращённое название', [validators.Length(min=1, max=10)])
    foundation_date = DateField('Дата основания', format='%Y-%m-%d', validators=[])

    def validate(self, **kwargs):
        if not Form.validate(self):
            return False
        if self.foundation_date.data > datetime.today():
            return False
        else:
            return True


class FoundationDateForm(Form):
    value = DateField('Дата основания', format='%Y-%m-%d')


class UniversityNameForm(Form):
    value = StringField('Полное наименование', [validators.Length(min=1, max=70)])


class UniversityShortNameForm(Form):
    value = StringField('Сокращенное название', [validators.Length(min=1, max=10)])
