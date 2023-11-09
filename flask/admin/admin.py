from enum import Enum
from flask import redirect, flash, url_for
from flask import request, render_template
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField

from admin.model import User  # Модель пользователя для работы с БД
from app import app, login_manager, db  # Импорт экземпляров приложения, менеджера логина и БД

# Перечисление для статусов аутентификации
class AuthStatus(Enum):
    Выйти = "/logout"
    Войти = "/login"

# Функция для загрузки пользователя, используется Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Форма входа на сайт с помощью WTForms
class LoginForm(FlaskForm):
    username = StringField('Пользователь')
    password = PasswordField('Пароль')

# Маршрут для страницы входа
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get("login")  # Получение логина из формы
    password = request.form.get("password")  # Получение пароля из формы

    # Проверка наличия логина и пароля
    if login and password:
        user = User.query.filter_by(login=login).first()  # Поиск пользователя в БД

        # Проверка соответствия хеша пароля и аутентификация пользователя
        if user and check_password_hash(user.password, password):
            login_user(user)  # Вход пользователя
            next_page = request.args.get('next')  # Получение URL для редиректа после входа

            return redirect(next_page) if next_page else redirect('/university')
        else:
            flash('Логин или пароль введены неверно')  # Сообщение об ошибке
    else:
        flash('Пожалуйста, заполните все поля')  # Сообщение о необходимости заполнения всех полей

    return render_template('login.html')  # Отображение страницы входа

# Маршрут для выхода из системы
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()  # Функция выхода пользователя
    return redirect(url_for('login_page'))  # Редирект на страницу входа

# Маршрут для страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')  # Получение логина из формы
    password = request.form.get('password')  # Получение пароля из формы
    password2 = request.form.get('password2')  # Получение подтверждения пароля

    # Обработка отправки формы
    if request.method == 'POST':
        # Валидация заполнения полей и совпадения паролей
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        elif User.query.filter_by(login=login).first():
            flash('Такой пользователь уже существует')
        else:
            # Создание хеша пароля и сохранение нового пользователя в БД
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))  # Редирект на страницу входа

    return render_template('register.html')  # Отображение страницы регистрации

# Функция для перенаправления неаутентифицированных пользователей на страницу входа
@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:  # Если статус ответа 401 (Не авторизован)
        return redirect(url_for('login_page') + '?next=' + request.url)  # Редирект с сохранением целевого URL

    return response  # Возврат неизмененного ответа, если статус не 401
