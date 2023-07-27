from fastapi import APIRouter

router = APIRouter(
    prefix="/geography",
    tags=["geography"],
)

from model import db
from model.common import Country
from pony.orm import *

db.generate_mapping(create_tables=True)

# region Country service

# Country pydantic model
from pydantic import BaseModel


class CountryModel(BaseModel):
    id: int = -1
    name_chs: str
    name_eng: str = ""
    fullname_eng: str = ""
    alphabet_code_2: str = ""
    alphabet_code_3: str = ""


# """get all country info result: list[country] format: name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic
# Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG"""
@router.get(path='/country/list',
            description="获取全部国家或地区列表。"
                        "格式：list[country]，"
                        "country示例：name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG"
            )
async def get_all_country():
    ret = []
    with db_session:
        country = Country.select()
        for c in country:
            ret.append(c.to_dict())

    return ret


@router.get(path='/country/{args}',
            description="通过id或名称查询国家或地区信息，名称可以是中文或英文名称。批量查询不同参数使用英文逗号,间隔。"
                        "格式：list[country]，"
                        "country示例：name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG")
async def get_country_by_name_or_id(args):
    ret = {'code': 404, 'msg': "没有查询到满足条件的结果", "paras": str(args)}

    with (db_session):
        if ',' in str(args):
            args = str(args).strip().split(',')
            country = select(c for c in Country if str(c.id) in args or c.name_chs in args or c.name_eng in args)
        else:
            country = select(c for c in Country if c.id == args or c.name_chs == args or c.name_eng == args)

        if country.count() > 0:
            ret = []
            for c in country:
                ret.append(c.to_dict())

    return ret


@router.post(path='/country/',
             summary="添加或更新国家或地区信息",
             description="添加国家或地区信息。不需要传入id值;更新国家或地区信息，必须传入id值。"
                         "格式：name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG")
async def add_country(args: CountryModel):
    ret = {'code': 403, 'msg': "待添加的信息已存在", "paras": str(args)}
    with db_session:
        # 添加

        if args.id is None or select(c for c in Country if c.id == args.id).count() <= 0:
            country = Country(name_chs=args.name_chs)
            country.name_eng = args.name_eng
            country.fullname_eng = args.fullname_eng
            country.alphabet_code_2 = args.alphabet_code_2
            country.alphabet_code_3 = args.alphabet_code_3

        try:
            country.flush()
            return {'code': 200, 'msg': "已添加", "result": country.to_dict()}
        except Exception as e:
            ret = {'code': 403, 'msg': str(e), "paras": str(args)}
            return ret

        # 更新




