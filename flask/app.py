from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5431/flask_education'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

login_manager = LoginManager(app)

from student.student import student_blueprint
from university.university import university_blueprint
from admin.admin import *

app.config['SECRET_KEY'] = 'secretkey'
app.register_blueprint(student_blueprint, url_prefix='/student')
app.register_blueprint(university_blueprint, url_prefix='/university')

if __name__ == '__main__':
    app.run()
