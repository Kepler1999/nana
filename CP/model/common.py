from model import db
from pony.orm import *

# region 地理位置
# --------------------------------
# 国家、省/州、城市、区县、乡镇街道
# 地址坐标


class Country(db.Entity):
    # 执行标准：GB/T 2659-2000
    __tablename__ = "common_geography_country"

    # base country information structure in GB/T 2659-2000
    name_chs = Required(str, unique=True, index=True)
    name_eng = Optional(str)
    fullname_eng = Optional(str)

    alphabet_code_2 = Optional(str)
    alphabet_code_3 = Optional(str)

    # you can extend in this
    # city = Set(lambda:City)


# class Province(db.Entity):
#     __tablename__ = 'common_geography_province'
#     # 本国语言名称
#     name = Required(str)
#     # 如果为外国，且不为中文或英文，可存中文或英文名称
#     name_chs = Optional(str)
#     name_eng = Optional(str)

#     country = Required("Country",reverse="province")

#     city = Set(lambda:City)


# class City(db.Entity):
#     __tablename__ = 'common_geography_city'
#     # 本国语言名称
#     name = Required(str)
#     # 如果为外国，且不为中文或英文，可存中文或英文名称
#     name_chs = Optional(str)
#     name_eng = Optional(str)

#     province  = Required("Province",reverse="city")

#     district = Set(lambda:District)

# class District(db.Entity):
#     __tablename__ = 'common_geography_district'
#     # 本国语言名称
#     name = Required(str)
#     # 如果为外国，且不为中文或英文，可存中文或英文名称
#     name_chs = Optional(str)
#     name_eng = Optional(str)

#     city = Required("City",reverse="district")

#     road_or_own = Set(lambda:RoadorTown)

# class RoadorTown(db.Entity):
#     __tablename__ = 'common_geography_road_or_own'

#     # 本国语言名称
#     name = Required(str)
#     # 如果为外国，且不为中文或英文，可存中文或英文名称
#     name_chs = Optional(str)
#     name_eng = Optional(str)

#     distinct = Required("District",reverse="road_or_own")

# class Coordinate(db.Entity):
#     __tablename__ = 'common_geography_coordinate'

#     # 经度
#     longitude = Required(str)
#     # 纬度
#     latitude = Required(str)
#     # 海拔
#     altitude = Optional(str)

# endregion


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
