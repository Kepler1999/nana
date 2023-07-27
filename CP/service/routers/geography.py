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
@router.get(
    path="/country/list",
    summary="获取全部国家或地区列表",
    description="格式：list[country]，"
    "country示例：name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG",
)
async def get_all_country():
    ret = {
        "code": 404,
        "msg": "没有查询到满足条件的结果",
        "data": [],
    }
    # with db_session:
    #     country = Country.select()
    #     if country.count() > 0:
    #         ret = ret = {
    #             "code": 200,
    #             "msg": f"{country.count()}条结果",
    #             "data": [],
    #         }
    #         for c in country:
    #             ret["data"].append(c.to_dict())

    with db_session:
        country = Country.select()
        ret = [c.to_dict() for c in country]

    return ret


@router.get(
    path="/country/{args}",
    summary="查询国家或地区信息",
    description="通过id或名称查询国家或地区信息，名称可以是中文或英文名称。批量查询多参数使用英文逗号,间隔",
)
async def get_country_by_name_or_id(args: int | str = -1):
    ret = {"code": 404, "msg": "没有查询到满足条件的结果", "paras": str(args)}

    filter = []

    with (db_session):
        args = str(args).replace("，", ",")
        args = args.strip().split(",")

        if isinstance(args, list):
            filter = args
        else:
            filter.append(args)

        country = select(
            cy
            for cy in Country
            if str(cy.id) in filter
            or str(cy.name_chs) in filter
            or str(cy.name_eng) in filter
        )

        ret = [c.to_dict() for c in country]

    return ret


@router.post(
    path="/country/",
    summary="添加或更新国家或地区信息",
    description="添加国家或地区信息。不需要传入id值"
    "格式：name_chs:阿富汗, name_eng:Afghanistan, fullname_eng:the Islamic Republic of Afghanistan, alphabet_code_2:AF, alphabet_code_3:AFG",
)
async def add_country(args: CountryModel):
    ret = {"code": 403, "msg": "待添加的信息已存在", "paras": str(args)}
    print(args)
    with db_session:
        # 添加
        country = Country(name_chs=args["name_chs"])
        # if (
        #     args.id is None
        #     or select(c for c in Country if c.id == args.id).count() <= 0
        # ):
        #     country = Country(
        #         name_chs=args.name_chs,
        #         name_eng=args.name_eng,
        #         fullname_eng=args.fullname_eng,
        #         alphabet_code_2=args.alphabet_code_2,
        #         alphabet_code_3=args.alphabet_code_3,
        #     )

        ret = {"code": 200, "msg": "已添加", "result": country.to_dict()}
        return ret

        # 更新
