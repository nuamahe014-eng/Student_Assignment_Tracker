from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, DateField
from wtforms.validators import DataRequired


class AssignmentForm(FlaskForm):

    title = StringField(
        "Assignment Title",
        validators=[DataRequired()]
    )

    course = StringField(
        "Course",
        validators=[DataRequired()]
    )

    deadline = DateField(
        "Deadline", format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed")
        ]
    )

    submit = SubmitField("Save Assignment")

class RegistrationForm(FlaskForm):

    username = StringField(
        "Username",
    validators=[DataRequired()]
    )

    email = StringField(
        "Email",
    validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
    validators=[DataRequired()]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
    validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
    validators=[DataRequired()]
    )

    submit = SubmitField("Login")

