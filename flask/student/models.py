from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    surname = db.Column(db.String(35), nullable=False)
    father_name = db.Column(db.String(40), nullable=True)
    entrance_year = db.Column(db.Integer, nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)