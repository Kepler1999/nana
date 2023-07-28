from fastapi import APIRouter
from pydantic import BaseModel
from pony.orm import *
from service.routers import db_session, Country


router = APIRouter(
    prefix="/geography",
    tags=["common-geography"],
)


# region Country service

# Country pydantic model


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
    with db_session:
        country = Country.select()
        ret = [c.to_dict() for c in country]

    return ret


@router.get(
    path="/country/",
    summary="查询国家或地区信息",
    description="通过id、中文名称、英文名称查询国家或地区信息。批量查询多参数使用英文逗号,间隔",
)
async def get_country_by_name_or_id(args: int | str = -1):
    ret = {"code": 404, "msg": "没有查询到满足条件的结果", "paras": str(args)}

    filter = []

    with db_session:
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
    summary="添加国家或地区信息",
    description="添加国家或地区信息，传入国家schema信息，id自动生成(不支持自定义）",
)
async def add_country(args: CountryModel):
    if len(str(args.name_chs).strip()) <= 0:
        return {"code": 401, "msg": "参数缺失:中文名称", "result": str(args)}

    with db_session:
        # 添加
        country = Country(
            name_chs=args.name_chs,
            name_eng=args.name_eng,
            fullname_eng=args.fullname_eng,
            alphabet_code_2=args.alphabet_code_2,
            alphabet_code_3=args.alphabet_code_3,
        )
        # country = Country(*args)
        ret = {"code": 200, "msg": "已添加", "result": country.to_dict()}
        return ret


@router.put(
    path="/country/",
    summary="更新国家或地区信息",
    description="更新国家或地区信息，传入国家schema信息，更新对应id的国家信息",
)
async def update_country(args: CountryModel):
    if len(str(args.id).strip()) <= 0:
        return {"code": 401, "msg": "参数缺失:id", "args": str(args)}

    with db_session:
        # 添加
        country = Country.get(id=args.id)

        if country is None:
            return {"code": 404, "msg": "未查找到符合条件的结果", "args": str(args)}

        if len(str(args.name_chs)) > 0:
            country.name_chs = args.name_chs

        if len(str(args.name_eng)) > 0:
            country.name_eng = args.name_eng

        if len(str(args.fullname_eng)) > 0:
            country.fullname_eng = args.fullname_eng

        if len(str(args.alphabet_code_2)) > 0:
            country.alphabet_code_2 = args.alphabet_code_2

        if len(str(args.alphabet_code_3)) > 0:
            country.alphabet_code_3 = args.alphabet_code_3

        ret = {"code": 200, "msg": "已更新", "result": country.to_dict()}

    return ret


@router.delete(
    path="/country/",
    summary="删除国家或地区信息",
    description="传入id,删除对应id的国家信息",
)
async def del_country(args: int):
    with db_session:
        # 添加
        country = Country.get(id=args.id)

        if country is None:
            return {"code": 404, "msg": "未查找到符合条件的结果", "args": str(args)}

        country.delete()

        ret = {"code": 200, "msg": "已更新", "result": country.to_dict()}

    return ret
