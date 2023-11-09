from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from wtforms import Form

from admin.admin import AuthStatus
from app import db
from student.forms import StudentForm, StudentNameForm, StudentSurnameForm, StudentFatherNameForm, \
    StudentEntranceYearForm, StudentUniversityIdForm
from student.models import Student
from university.models import University

# Инициализация Blueprint для маршрутизации студенческого модуля
student_blueprint = Blueprint(
    'student_blueprint',
    __name__,
    template_folder='template',
    static_folder='static'
)

# Маршрут и обработчик для создания новой записи студента
@student_blueprint.route('/create', methods=['GET', 'POST'])
@login_required  # Проверка на аутентификацию пользователя
def student_create():
    if request.method == 'POST':
        # Создание нового объекта студента с данными из формы
        stud = Student(
            name=request.form['name'],
            surname=request.form['surname'],
            father_name=request.form['father_name'],
            entrance_year=request.form['entrance_year'],
            university_id=request.form['university_id']
        )
        # Добавление объекта студента в сессию БД и сохранение изменений
        db.session.add(stud)
        db.session.commit()
        # Перенаправление на страницу со списком студентов
        return redirect("/student")
    else:
        # Если метод GET, предоставляем форму для создания студента
        s = StudentForm()
        s.university_id.choices = [
            (u.id, u.name) for u in University.query.order_by('name')
        ]
        return render_template('student/create.html', form=s)

# Маршрут для удаления записи студента
@student_blueprint.route('/delete/<int:student_id>')
@login_required
def student_delete(student_id):
    # Удаление студента по ID и сохранение изменений в БД
    Student.query.filter_by(id=student_id).delete()
    db.session.commit()
    return redirect('/student')

# Маршрут для отображения списка всех студентов
@student_blueprint.route('/')
def student_list():
    # Получение всех записей студентов из БД
    all_students = Student.query.all()
    # Отправка изменений в БД (может быть не нужно, если только читаем данные)
    db.session.commit()

    # Отображение разных шаблонов в зависимости от статуса аутентификации пользователя
    try:
        if current_user.login:
            return render_template(
                'student/student_list.html',
                items=all_students,
                auth_status=AuthStatus.Выйти,  # Статус для кнопки выхода
                login=current_user.login
            )
    except AttributeError:
        # Если аутентификация не пройдена, предлагаем войти
        return render_template(
            'student/student_list.html',
            items=all_students,
            auth_status=AuthStatus.Войти,  # Статус для кнопки входа
            login=""
        )

# Вспомогательная функция для проверки корректности года поступления
def is_bad_entrance_year(year: int, student_id: int) -> bool:
    return University.query.filter_by(
        id=Student.query
        .filter_by(id=student_id)
        .first()
        .university_id
    ).first().foundation_date.year > year

# Вспомогательная функция для создания формы в зависимости от имени поля
def form_by_field_name(field_name: str) -> Form:
    match field_name:
        case 'name':
            return StudentNameForm()
        case 'surname':
            return StudentSurnameForm()
        case 'father_name':
            return StudentFatherNameForm()
        case 'entrance_year':
            return StudentEntranceYearForm()
        case 'university_id':
            s = StudentUniversityIdForm()
            s.value.choices = [
                (u.id, u.name) for u in University.query.order_by('name')
            ]
            return s


# Вспомогательная функция для создания формы в зависимости от имени поля
def is_bad_university_id(student_id: int, university_id: int) -> bool:
    stud = Student.query.filter_by(id=student_id).first()
    university = University.query.filter_by(id=university_id).first()
    return university.foundation_date.year > stud.entrance_year


# Маршрут для обновления данных студента, требует аутентификации пользователя
@student_blueprint.route('/update/<int:student_id>/<field_name>', methods=["GET", "POST"])
@login_required
def student_update(student_id: int, field_name: str):
    # Если данные отправлены методом POST (из формы)
    if request.method == "POST":
        # Получаем объект запроса фильтрации по ID студента
        filter = Student.query.filter_by(id=student_id)
        # Получаем значение из отправленной формы
        value = request.form["value"]

        # Сопоставление имени поля с действием для обновления соответствующего атрибута
        match field_name:
            case 'name':
                filter.first().name = value
            case 'surname':
                filter.first().surname = value
            case 'father_name':
                filter.first().father_name = value
            case 'entrance_year':
                year = int(value)
                # Проверка допустимости года поступления
                if is_bad_entrance_year(year, student_id):
                    # Если проверка не пройдена, возвращаем ошибку
                    return render_template("student/uniform.html", items={
                        "link": "/student",
                        "text": 'Теперь ваши студенты обучаются в вузе, который основан после их поступления'
                    })
                else:
                    filter.first().entrance_year = year
            case 'university_id':
                university_id = int(value)
                # Проверка соответствия ID университета и года поступления
                if is_bad_university_id(student_id, university_id):
                    # Если проверка не пройдена, возвращаем ошибку
                    return render_template("student/uniform.html", items={
                        "link": "/university",
                        "text": 'Теперь ваши студенты обучаются в вузе, который основан после их поступления'
                    })
                else:
                    filter.first().university_id = university_id

        # Применяем изменения в базе данных
        db.session.commit()
        # Перенаправляем на страницу списка студентов
        return redirect("/student")
    else:
        # Если метод GET, отображаем форму для обновления
        return render_template(
            "student/update.html",
            form=form_by_field_name(field_name),
            id=student_id,
            field_name=field_name
        )

# Маршрут для отображения информации о конкретном студенте
@student_blueprint.route('/<int:student_id>')
def student_detail(student_id: int):
    # Словарь данных для передачи в шаблон
    data = {'link': '/student'}

    try:
        # Получение объекта студента по ID
        curr_student = Student.query.get(student_id)
        # Обновление словаря данными студента
        data.update({"text": f"{curr_student.name}"})
    except (SQLAlchemyError, AttributeError):
        # Обработка исключения, если студент не найден
        data.update({"text": "Студента с таким id не существует"})

    # Отображаем шаблон с информацией о студенте или ошибкой
    return render_template("student/uniform.html", items=data)

