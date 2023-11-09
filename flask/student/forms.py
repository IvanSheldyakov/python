import datetime

from wtforms import IntegerField, SelectField, StringField, Form, validators
from wtforms.validators import DataRequired, NumberRange


class StudentForm(Form):
    name = StringField('Имя', [validators.length(min=1, max=35)])
    surname = StringField('Фамилия', [validators.length(min=1, max=35)])
    father_name = StringField('Отчество', [validators.length(min=1, max=40)])
    entrance_year = IntegerField(u'Год поступления', validators=[
        DataRequired(),
        NumberRange(max=datetime.date.today().year)
    ])
    university_id = SelectField(u'Университет', coerce=int)


class StudentNameForm(Form):
    value = StringField('Имя', [validators.length(min=1, max=35)])


class StudentSurnameForm(Form):
    value = StringField('Фамилия', [validators.length(min=1, max=35)])


class StudentFatherNameForm(Form):
    value = StringField('Отчество', [validators.length(min=1, max=40)])


class StudentEntranceYearForm(Form):
    value = IntegerField(u'Год поступления', validators=[
        DataRequired(),
        NumberRange(max=datetime.date.today().year)
    ])


class StudentUniversityIdForm(Form):
    value = SelectField(u'Университет', coerce=int)
