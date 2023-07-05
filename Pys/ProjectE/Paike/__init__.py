from pony.orm import *

db = Database()

class Table(db.Entity):
    week = Required(int)
    day_index = Required(int)

    course = Optional("Course")


class Teacher(db.Entity):
    pass

class Clas(db.Entity):
    pass

class Course(db.Entity):
    code = Required(int)
    name = Required(str)

    teacher = Required(Teacher)
    student = Required(Clas)


class Arrangement(db.Entity):
    week = 1