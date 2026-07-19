from flask import Flask, render_template, redirect, url_for, flash
from datetime import datetime
from models import db, Assignment, User
from forms import AssignmentForm, RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config['SECRET_KEY'] = "student_tracker_secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

@app.route("/")
@login_required
def home():

    assignments = Assignment.query.filter_by(
        user_id=current_user.id
    ).all()

    today = datetime.today().date()

    for assignment in assignments:

        if (
            assignment.deadline < today
            and assignment.status != "Completed"
        ):
            assignment.status = "Overdue"

    db.session.commit()

    total = len(assignments)

    pending = len([
        a for a in assignments
        if a.status == "Pending"
    ])

    completed = len([
        a for a in assignments
        if a.status == "Completed"
    ])

    overdue = len([
        a for a in assignments
        if a.status == "Overdue"
    ])

    return render_template(
        "index.html",
        assignments=assignments,
        total=total,
        pending=pending,
        completed=completed,
        overdue=overdue
    )



@app.route("/delete/<int:id>")
@login_required
def delete_assignment(id):  

    assignment = Assignment.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    db.session.delete(assignment)
    db.session.commit()

    flash("Assignment deleted successfully!", "danger")

    return redirect(url_for("home"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_assignment(id):

    assignment = Assignment.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    form = AssignmentForm()

    if form.validate_on_submit():

        assignment.title = form.title.data
        assignment.course = form.course.data
        assignment.deadline = form.deadline.data
        assignment.status = form.status.data

        db.session.commit()

        flash("Assignment updated successfully", "success")

        return redirect(url_for("home"))

    form.title.data = assignment.title
    form.course.data = assignment.course
    form.deadline.data = assignment.deadline
    form.status.data = assignment.status

    return render_template(
        "edit_assignment.html",
        form=form
    )




@app.route("/add", methods=["GET", "POST"])
@login_required
def add_assignment():

    form = AssignmentForm()

    if form.validate_on_submit():

        assignment = Assignment(
            title=form.title.data,
            course=form.course.data,
            deadline=form.deadline.data,
            status=form.status.data,
            user_id=current_user.id
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Assignment added successfully!", "success")

        return redirect(url_for("home"))

    return render_template(
        "add_assignment.html",
        form=form
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")

        return redirect(url_for("home"))

    return render_template(
        "register.html",
        form=form
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("home"))

        else:
            flash("Invalid email or password", "danger")


    return render_template(
        "login.html",
        form=form
    )

@app.route("/logout")
def logout():

    logout_user()

    flash("You have been logged out successfully!", "success")

    return redirect(url_for("login"))

@app.route("/complete/<int:id>")
@login_required
def complete_assignment(id):

    assignment = Assignment.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    assignment.status = "Completed"

    db.session.commit()

    flash("Assignment marked as completed!", "success")

    return redirect(url_for("home"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)