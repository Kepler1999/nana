from model import db
from pony.orm import *
from datetime import date, datetime


# region 学校网站配置
class School(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)
    description = Optional(str)

    web_sites = Set("WebSite")
    customer_type = Optional(int)  # 1:十一系客户 2：普通客户 -1：内部测试
    business_status = Optional(int)  # -1：试用客户 1:付费客户  2.复购客户  3.流失待挽留客户 4.丢失客户  5.重获客户

    create_at = Optional(float, default=datetime.timestamp(datetime.now()))
    is_delete = Optional(bool, default=False)


class WebSite(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)
    domain = Optional(str)
    description = Optional(str)

    school = Optional(School)
    modules = Set("Module")

    type = Optional(
        int
    )  # 1：Business Software 2：Trail Software 3: Free Software  -1：Insider Alpha/Beta Software 0：Demonstration Software

    create_at = Optional(float, default=datetime.timestamp(datetime.now()))
    is_delete = Optional(bool, default=False)


class Module(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)
    description = Optional(str)

    web_site = Required(WebSite)
    submodules = Set("Submodule")

    create_at = Optional(float, default=datetime.timestamp(datetime.now()))
    is_delete = Optional(bool, default=False)


class Submodule(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)
    description = Optional(str)

    module = Required(Module)
    pages = Set("Page")

    create_at = Optional(float, default=datetime.timestamp(datetime.now()))
    is_delete = Optional(bool, default=False)


class Page(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)
    description = Optional(str)
    uri = Optional(str, unique=True)

    submodule = Required(Submodule)

    create_at = Optional(float, default=datetime.timestamp(datetime.now()))
    is_delete = Optional(bool, default=False)

    pv = Optional(int)
    uv = Optional(int)


# endregion
if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
