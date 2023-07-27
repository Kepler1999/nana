from fastapi import APIRouter

router = APIRouter(
    prefix="/place",
    tags=["place"],
)

@router.get('/')
async def palce():
    return {'2':'go'}


# import sys,os
# PROJ_DIR = "Pys\ProjectE\CloudE"
# sys.path.append(os.path.join(PROJ_DIR, 'project'))

# from server import db
# from pony.orm import *

# class Country(db.Entity):
#     # 执行标准：GB/T 2659-2000
#     __tablename__ = 'common_geography_country'
    
#     # base country information structure in GB/T 2659-2000
#     name_chs = Required(str,unique=True,index=True)
#     name_eng = Optional(str)
#     fullname_eng = Optional(str)
    
#     alphabet_code_2 = Required(str)
#     alphabet_code_3 = Optional(str)
    
#     # you can extend in this    
#     # city = Set(lambda:City)

# @router.get('/country/list')
# async def country_list():
#     ret = []
#     with db_session:
#         country = Country.select()
#         for c in country[:]:
#             ret.append(c.to_dict())
    
#     return ret