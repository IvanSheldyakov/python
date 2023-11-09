from django import forms
import datetime


class StudentRegistrationForm(forms.Form):
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    patronymic = forms.CharField(label='Отчество')
    year_of_admission = forms.IntegerField(label='Год поступления', min_value=1984, max_value=datetime.date.today().year)
    uni_acronym = forms.CharField(label='Вуз', max_length=10)


class UniversityForm(forms.Form):
    full_name = forms.CharField(label='Полное наименование')
    acronym = forms.CharField(label='Сокращённое название')
    establishment_date = forms.DateField(label='Дата основания',
                                         widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                         required=True)


class StudentUpdateForm(forms.Form):
    student_id = forms.IntegerField(label="Id")
    update_field_choices = (
        ('', 'Выберите параметр'),
        ('last_name', 'Фамилия'),
        ('first_name', 'Имя'),
        ('patronymic', 'Отчество'),
        ('year_of_admission', 'Год поступления'),
        ('uni_acronym', 'Вуз')
    )
    update_field = forms.ChoiceField(label="Поле", choices=update_field_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    new_value = forms.CharField(label="Новое значение")


class UniversityUpdateForm(forms.Form):
    university_id = forms.IntegerField(label="Id")
    update_field_choices = (
        ('', 'Выберите параметр'),
        ('full_name', 'Полное название'),
        ('acronym', 'Краткое название'),
        ('establishment_date', 'Дата основания')
    )
    update_field = forms.ChoiceField(label="Поле", choices=update_field_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    new_value = forms.CharField(label="Новое значение")
