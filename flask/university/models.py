from app import db


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    foundation_date = db.Column(db.Date, nullable=False)
    students = db.relationship('Student', backref='university')
