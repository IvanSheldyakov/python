import datetime

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from wtforms import Form

from admin.admin import AuthStatus
from app import db
from student.models import Student
from university.forms import UniversityForm, FoundationDateForm, UniversityNameForm, UniversityShortNameForm
from university.models import University

university_blueprint = Blueprint(
    'university_blueprint',
    __name__,
    template_folder='template',
    static_folder='static'
)


# Маршрут для создания университета с декоратором для требования входа в систему
@university_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def university_create():
    if request.method == 'POST':
        # Если метод POST, создаем новый объект University и сохраняем в базе данных
        uni1 = University(
            name=request.form['name'],
            short_name=request.form['short_name'],
            foundation_date=request.form['foundation_date']
        )
        db.session.add(uni1)
        db.session.commit()
        return redirect("/university")
    else:
        # Если метод не POST, отображаем форму для создания университета
        return render_template('university/create.html', form=UniversityForm())


# Маршрут для удаления университета, также требует входа в систему
@university_blueprint.route('/delete/<int:university_id>')
@login_required
def university_delete(university_id):
    try:
        # Пытаемся удалить университет и сохранить изменения в базе данных
        University.query.filter_by(id=university_id).delete()
        db.session.commit()
        return redirect('/university')
    except SQLAlchemyError:
        # Если произошла ошибка, предположительно связанная с наличием студентов, сообщаем об этом
        data = {"link": "/university"}
        data.update({"text": "Университет нельзя удалить, т.к. там ещё числятся студенты."})
        return render_template("university/uniform.html", items=data)



# Маршрут для отображения списка университетов
@university_blueprint.route('/')
def university_list():
    all_universities = University.query.all()
    db.session.commit()
    # Проверяем, залогинен ли пользователь, и отображаем соответствующую страницу
    try:
        if current_user.login:
            return render_template(
                "university/university_list.html",
                items=all_universities,
                auth_status=AuthStatus.Выйти,
                login=current_user.login
            )
    except AttributeError:
        return render_template(
            "university/university_list.html",
            items=all_universities,
            auth_status=AuthStatus.Войти,
            login=""
        )

# Функция возвращает форму в зависимости от переданного имени поля
def form_by_field_name(field_name: str) -> Form:
    match field_name:
        case 'foundation_date':
            return FoundationDateForm()
        case 'name':
            return UniversityNameForm()
        case 'short_name':
            return UniversityShortNameForm()


# Функция для проверки корректности даты основания университета
def is_bad_foundation_date(year: int, university_id: int) -> bool:
    students = Student.query.filter_by(university_id=university_id)

    # Если нет студентов, то дата корректна
    if students.count() == 0:
        return False

    # Если есть студенты, которые поступили до основания университета, дата некорректна
    return students.filter(Student.entrance_year < year).count() > 0


# Маршрут для обновления данных университета
@university_blueprint.route('/update/<int:university_id>/<field_name>', methods=["GET", "POST"])
@login_required
def university_update(university_id: int, field_name: str):
    if request.method == "POST":
        filter = University.query.filter_by(id=university_id)
        value = request.form["value"]

        # С помощью оператора match обновляем поля университета
        match field_name:
            case 'name':
                filter.first().name = value
            case 'short_name':
                filter.first().short_name = value
            case 'foundation_date':
                year = datetime.datetime.strptime(value, '%Y-%m-%d').year

                # Проверяем корректность даты основания перед обновлением
                if (is_bad_foundation_date(year, university_id)):
                    return render_template("university/uniform.html", items={
                        "link": "/university",
                        "text": 'Теперь ваши студенты обучаются в вузе, который основан после их поступления'
                    })
                else:
                    filter.first().foundation_date = value

        # Сохраняем изменения в базе данных
        db.session.commit()
        return redirect("/university")
    else:
        # Если метод не POST, отображаем форму для обновления данных
        return render_template(
            "university/update.html",
            form=form_by_field_name(field_name),
            id=university_id,
            field_name=field_name
        )


# Маршрут для просмотра информации об одном университете
@university_blueprint.route('/<int:university_id>')
def university(university_id: int):
    data = {"link": "/university"}

    try:
        # Пытаемся получить данные университета по ID
        curr_university = University.query.get(university_id)
        data.update({"text": f"{curr_university.name}"})
    except (SQLAlchemyError, AttributeError):
        # В случае ошибки выводим сообщение, что университет не найден
        data.update({"text": "Университета с таким id не существует"})

    return render_template("university/uniform.html", items=data)

