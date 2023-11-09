import datetime

from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.exceptions import ValidationError

from educational_service import forms, models

# Главная страница
def index(request):
    return render(request, "index.html")

# Представление студента
def student(request, student_id):
    # Получение студента или 404
    curr_student = get_object_or_404(models.Student, id=student_id)
    data = {
        "student_surname": curr_student.surname,
        "student_name": curr_student.name,
        "student_father_name": curr_student.father_name,
        "student_entrance_year": curr_student.entrance_year,
        "student_university": curr_student.university
    }
    return render(request, "student.html", data)

# Представление университета
def university(request, university_id):
    # Получение университета или 404
    curr_university = get_object_or_404(models.University, id=university_id)
    data = {
        "university_name": curr_university.name,
        "university_short_name": curr_university.short_name,
        "university_foundation_date": curr_university.foundation_date
    }
    return render(request, "university.html", data)

# Создание студента
def create_student(request):
    if request.method == "POST":
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Перенаправление на страницу детального представления студента
            return HttpResponseRedirect(reverse('student_detail', args=[student.id]))
        return HttpResponseBadRequest("Некорректный ввод.")
    else:
        form = forms.StudentForm()
    return render(request, "create_student.html", {'form': form})

# Создание университета
def create_university(request):
    if request.method == "POST":
        form = forms.UniversityForm(request.POST)
        if form.is_valid():
            university = form.save()
            # Перенаправление на страницу детального представления университета
            return HttpResponseRedirect(reverse('university_detail', args=[university.id]))
        return HttpResponseBadRequest("Некорректный ввод.")
    else:
        form = forms.UniversityForm()
    return render(request, "create_university.html", {'form': form})

# Удаление студента
def delete_student(request, student_id):
    student = get_object_or_404(models.Student, id=student_id)
    student.delete()
    return HttpResponseRedirect(reverse('students_list'))

# Удаление университета
def delete_university(request, university_id):
    university = get_object_or_404(models.University, id=university_id)
    university.delete()
    return HttpResponseRedirect(reverse('universities_list'))

# Список студентов
def students_list(request):
    all_students = models.Student.objects.all()
    return render(request, "student_list.html", {"students": all_students})

# Список университетов
def university_list(request):
    all_universities = models.University.objects.all()
    return render(request, "university_list.html", {"universities": all_universities})


# Функция для обновления данных студента
def student_update(request, student_id: int, field_name: str):
    # Получение объекта студента, иначе возвращает 404
    student = get_object_or_404(models.Student, id=student_id)
    # Получение значения из параметров запроса
    value = request.GET.get("value")

    # Если поле для обновления - университет, выполняем дополнительные проверки
    if field_name == 'university':
        # Поиск университета по короткому названию
        university = get_object_or_404(models.University, short_name=value)
        # Проверяем, что год основания университета не позже года поступления студента
        if university.foundation_date.year > student.entrance_year:
            return HttpResponseBadRequest("Вуз не мог быть основан после поступления студента.")
        # Если проверка прошла успешно, устанавливаем университет как значение для обновления
        value = university

    # Пытаемся обновить значение поля и сохранить объект
    try:
        setattr(student, field_name, value) # Установка значения поля
        student.full_clean() # Валидация объекта
        student.save() # Сохранение изменений в базе данных
        # Перенаправление на страницу деталей студента после успешного обновления
        return HttpResponseRedirect(reverse('student_detail', args=[student.id]))
    # Обработка возможных исключений при валидации или установке значения
    except (ValidationError, ValueError):
        return HttpResponseBadRequest("Плохое значение.")

# Функция для обновления данных университета
def university_update(request, university_id: int, field_name: str):
    # Получение объекта университета, иначе возвращает 404
    university = get_object_or_404(models.University, id=university_id)
    # Получение значения из параметров запроса
    value = request.GET.get("value")

    # Если обновляемое поле - дата основания, выполняем дополнительные проверки
    if field_name == 'foundation_date':
        # Преобразуем строку в дату
        foundation_date = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        # Проверяем, что дата основания не в будущем
        if foundation_date > datetime.date.today():
            return HttpResponseBadRequest("Вуз не мог основаться в будущем.")

    # Пытаемся обновить значение поля и сохранить объект
    try:
        setattr(university, field_name, value) # Установка значения поля
        university.full_clean() # Валидация объекта
        university.save() # Сохранение изменений в базе данных
        # Перенаправление на страницу деталей университета после успешного обновления
        return HttpResponseRedirect(reverse('university_detail', args=[university.id]))
    # Обработка возможных исключений при валидации или установке значения
    except (ValidationError, ValueError):
        return HttpResponseBadRequest("Невалидное значение.")

# Представление для страницы обновления данных студента
def updator_student(request):
    # Обработка POST-запроса для обновления данных
    if request.method == "POST":
        return updator_post_action(request, "student")
    # Если метод GET, отображаем форму для ввода данных
    form = forms.StudentUpdateForm()
    return render(request, "make_update.html", {"title": "студент", "form": form})

# Представление для страницы обновления данных университета
def updator_university(request):
    # Обработка POST-запроса для обновления данных
    if request.method == "POST":
        return updator_post_action(request, "university")
    # Если метод GET, отображаем форму для ввода данных
    form = forms.UniversityUpdateForm()
    return render(request, "make_update.html", {"title": "университет", "form": form})

# Функция, обрабатывающая POST-запрос для обновления данных
def updator_post_action(request, category):
    # Получение данных из POST-запроса
    id = request.POST.get('id')
    field_name = request.POST.get('field_name')
    value = request.POST.get('value')
    # Формирование URL для перенаправления с параметрами запроса
    redirect_url = reverse(f'{category}_update', args=[id, field_name]) + f"?value={value}"
    # Выполнение перенаправления
    return HttpResponseRedirect(redirect_url)