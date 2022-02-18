from enum import unique
import os
from re import I
from flask import Flask, redirect
from flask import render_template, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey(
        "student.student_id"), primary_key=True, nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey(
        "course.course_id"), primary_key=True, nullable=False)


@ app.route("/", methods=['GET', 'POST'])
def home():
    students = Student.query.all()
    empt = students == []
    return render_template("index.html", students=students, empt=empt)


@ app.route("/student/create", methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        roll_no = (request.form.get("roll"))
        first_name = request.form.get("f_name")
        last_name = request.form.get("l_name")
        courses = request.form.getlist('courses')
        print(courses)

        # User.query.filter_by(username='peter')
        is_student = Student.query.filter_by(roll_number=int(roll_no)).all()
        print(is_student, roll_no)
        if not request.form['roll'] or not request.form['f_name'] or not request.form['l_name'] or not courses:
            print('Please enter all the fields', 'error')
        elif(not (is_student == [])):
            return render_template("createalready.html")
        else:

            student = Student(roll_number=int(roll_no),
                              first_name=first_name, last_name=last_name)

            db.session.add(student)
            db.session.commit()
            for course in courses:
                if course == "course_1":
                    Enroll = Enrollments(
                        estudent_id=student.student_id, ecourse_id=1)
                    db.session.add(Enroll)
                    db.session.commit()
                elif course == "course_2":
                    Enroll = Enrollments(
                        estudent_id=student.student_id, ecourse_id=2)
                    db.session.add(Enroll)
                    db.session.commit()
                elif course == "course_3":
                    Enroll = Enrollments(
                        estudent_id=student.student_id, ecourse_id=3)
                    db.session.add(Enroll)
                    db.session.commit()
                elif course == "course_4":
                    Enroll = Enrollments(
                        estudent_id=student.student_id, ecourse_id=4)
                    db.session.add(Enroll)
                    db.session.commit()
                else:
                    print('Please enter all the course correctly', 'error')

                print('Record was successfully added')
            return redirect(url_for('home'))
    return render_template('index.html')


@ app.route("/student/<roll_no>/delete", methods=['GET', 'POST'])
def delete(roll_no):
    student = Student.query.filter_by(student_id=int(roll_no)).first()
    if type(student) != None:
        db.session.delete(student)
        db.session.commit()
    enroll = Enrollments.query.filter_by(estudent_id=int(roll_no)).all()
    for enrol in enroll:
        db.session.delete(enrol)
        db.session.commit()
    return redirect(url_for('home'))


@ app.route("/student/<roll_no>/update", methods=['GET', 'POST'])
def update(roll_no):
    if request.method == "GET":
        student = Student.query.filter_by(student_id=int(roll_no)).first()
        print(student)
        return render_template('update.html', student=student)
    if request.method == "POST":
        enroll = Enrollments.query.filter_by(estudent_id=int(roll_no)).all()
        for enrol in enroll:
            db.session.delete(enrol)
            db.session.commit()
        student = Student.query.filter_by(student_id=int(roll_no)).first()
        if request.form.get("f_name"):
            student.first_name = request.form.get("f_name")
            db.session.commit()
        if request.form.get("l_name"):
            student.last_name = request.form.get("l_name")
            db.session.commit()

        courses = request.form.getlist('courses')
        for course in courses:
            if course == "course_1":
                Enroll = Enrollments(
                    estudent_id=student.student_id, ecourse_id=1)
                db.session.add(Enroll)
                db.session.commit()
            elif course == "course_2":
                Enroll = Enrollments(
                    estudent_id=student.student_id, ecourse_id=2)
                db.session.add(Enroll)
                db.session.commit()
            elif course == "course_3":
                Enroll = Enrollments(
                    estudent_id=student.student_id, ecourse_id=3)
                db.session.add(Enroll)
                db.session.commit()
            elif course == "course_4":
                Enroll = Enrollments(
                    estudent_id=student.student_id, ecourse_id=4)
                db.session.add(Enroll)
                db.session.commit()
            else:
                print('Please enter all the course correctly', 'error')
        return redirect(url_for('home'))


@ app.route("/student/<roll_name>", methods=['GET', 'POST'])
def homi(roll_name):
    student = Student.query.filter_by(student_id=int(roll_name)).first()
    enroll = Enrollments.query.filter_by(estudent_id=int(roll_name)).all()
    relev_courseid = []
    for enrol in enroll:
        relev_courseid.append(enrol.ecourse_id)
    courses = Course.query.filter(Course.course_id.in_(relev_courseid)).all()
    return render_template("studentdetail.html", student=student, course=courses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
