from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    assignments = db.relationship(
        "Assignment",
        backref="user",
        lazy=True
    )

class Assignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    course = db.Column(db.String(100), nullable=False)

    deadline = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(50), default="Pending")

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=True
)


    def __repr__(self):
        return f"Assignment('{self.title}')"