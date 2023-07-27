from _db import db
from pony.orm import *

from datetime import date
from datetime import datetime


class School(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    desc = Optional(str)
    buildings = Set('Building')
    departmentss = Set('Departments')
    teachyears = Set('Teachyear')
    categorys = Set('Category')
    grades = Set('Grade')


class Departments(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    school = Required(School)


class Building(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    school = Required(School)
    rooms = Set('Room')


class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    code = Optional(str)
    size = Optional(float)
    volume = Optional(int)
    type = Optional(int)
    floor = Optional(int)
    building = Required(Building)
    course_classses = Set('Course_class')


class Person(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    gender = Optional(int)
    birthday = Optional(date)


class Student(Person):
    stu_code = Optional(str)
    entry_at = Optional(datetime)
    graduate_at = Optional(datetime)
    administrative_classes = Set('Administrative_class')
    course_classses = Set('Course_class')
    exam_scores = Set('Exam_score')
    semester_grades = Set('Semester_grade')
    parenets = Set('Parenet')


class Employee(Person):
    work_code = Optional(str)
    type = Optional(int)
    course_classses = Set('Course_class')
    charging_banji = Set('Administrative_class')


class Teachyear(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    start_at = Optional(date)
    finish_at = Optional(date)
    semesters = Set('Semester')
    course_classses = Set('Course_class')
    school = Required(School)


class Semester(db.Entity):
    id = PrimaryKey(int, auto=True)
    teachyear = Required(Teachyear)
    administrative_classes = Set('Administrative_class')
    course_classses = Set('Course_class')
    sections = Set('Section')
    exams = Set('Exam')
    semester_grades = Set('Semester_grade')


class Course(db.Entity):
    id = PrimaryKey(int, auto=True)
    subject = Required('Subject')
    course_classses = Set('Course_class')


class Subject(db.Entity):
    id = PrimaryKey(int, auto=True)
    category = Optional('Category')
    courses = Set(Course)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    subjects = Set(Subject)
    school = Required(School)


class Administrative_class(db.Entity):
    id = PrimaryKey(int, auto=True)
    students = Set(Student)
    semester = Required(Semester)
    tutor = Set(Employee)
    name = Optional(str)


class Course_class(db.Entity):
    id = PrimaryKey(int, auto=True)
    semester = Required(Semester)
    teachyears = Set(Teachyear)
    rooms = Set(Room)
    course = Required(Course)
    employees = Set(Employee)
    students = Set(Student)
    exams = Set('Exam')
    exam_scores = Set('Exam_score')


class Grade(db.Entity):
    id = PrimaryKey(int, auto=True)
    grade = Optional(int)
    name = Optional(str)
    semester_grades = Set('Semester_grade')
    school = Required(School)


class Exam(db.Entity):
    id = PrimaryKey(int, auto=True)
    exam_at = Optional(datetime)
    name = Optional(str)
    semester = Optional(Semester)
    course_classses = Set(Course_class)
    exam_scores = Set('Exam_score')


class Section(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    sort = Optional(int)
    semester = Required(Semester)


class Exam_score(db.Entity):
    id = PrimaryKey(int, auto=True)
    present_score = Optional(float)
    student = Required(Student)
    exam = Required(Exam)
    course_class = Required(Course_class)
    test_score = Optional(str)
    makeup_score = Optional(str)


class Semester_grade(db.Entity):
    id = PrimaryKey(int, auto=True)
    students = Set(Student)
    semesters = Set(Semester)
    grades = Set(Grade)


class Parenet(Person):
    students = Set(Student)




if __name__ == '__main__':
    db.generate_mapping(create_tables=True)