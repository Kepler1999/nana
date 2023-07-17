from _db import db
from pony.orm import *

# region 地理位置
# --------------------------------
# 国家、省/州、城市、区县、乡镇街道
# 地址坐标

class Country(db.Entity):
    __tablename__ = 'common_geography_country'
    # 中文全称
    name_chs = Required(str)
    # 中文简称：中国
    name_chs_abbr = Optional(str)
    # 英文全称
    name_eng = Optional(str)    
    # 英文简称
    name_eng_abbr = Optional(str)   
    # 本国语言全称,如果为外国，且不为中文或英文，可存此字段
    name = Optional(str)
        
    province = Set(lambda:Province)

class Province(db.Entity):
    __tablename__ = 'common_geography_province'    
    # 本国语言名称
    name = Required(str)
    # 如果为外国，且不为中文或英文，可存中文或英文名称
    name_chs = Optional(str)
    name_eng = Optional(str)
    
    country = Required("Country",reverse="province")
    
    city = Set(lambda:City)


class City(db.Entity):
    __tablename__ = 'common_geography_city'     
    # 本国语言名称
    name = Required(str)
    # 如果为外国，且不为中文或英文，可存中文或英文名称
    name_chs = Optional(str)
    name_eng = Optional(str)
    
    province  = Required("Province",reverse="city")
    
    district = Set(lambda:District)

class District(db.Entity):
    __tablename__ = 'common_geography_district'
    # 本国语言名称
    name = Required(str)
    # 如果为外国，且不为中文或英文，可存中文或英文名称
    name_chs = Optional(str)
    name_eng = Optional(str)
    
    city = Required("City",reverse="district")
    
    road_or_own = Set(lambda:RoadorTown)

class RoadorTown(db.Entity):
    __tablename__ = 'common_geography_road_or_own'
    
    # 本国语言名称
    name = Required(str)
    # 如果为外国，且不为中文或英文，可存中文或英文名称
    name_chs = Optional(str)
    name_eng = Optional(str)
    
    distinct = Required("District",reverse="road_or_own")

class Coordinate(db.Entity):
    __tablename__ = 'common_geography_coordinate'
    
    # 经度
    longitude = Required(str)
    # 纬度
    latitude = Required(str)
    # 海拔
    altitude = Optional(str)

# endregion

if __name__ == '__main__':
    db.generate_mapping(create_tables=True)