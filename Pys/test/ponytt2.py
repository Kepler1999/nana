from ponytest import db, func_exec_time
from pony.orm import *


class Category(db.Entity):
    type = Required(str)
    name = Required(str)
    desc = Optional(str)

    parent_category = Required(int)


if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    with db_session():
        c1 = Category(type="综合课程", name="生活技能", parent_category=0)
        c1.flush()

        c2 = Category(type="综合课程", name="厨艺", parent_category=c1.id)


        o = select( i for i in Category if i.parent_category !=0 )
        for x in o:
            print(x.type,x.name,x.desc,x.parent_category)
            pare = select( a for a in Category if a.id == x.parent_category)
            for i in pare:
                print(i.type, i.name, i.desc, i.parent_category)
