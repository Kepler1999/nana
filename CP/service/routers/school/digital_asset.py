from fastapi import APIRouter
from service.tools import get_id
from service.routers import db_session, School, WebSite, Module, Submodule, Page

from pydantic import BaseModel
from pony.orm import *

router = APIRouter(
    prefix="/school/digital_asset",
    tags=["school-basement-digital-asset"],
)


# region pydantic model map
class SchoolModel(BaseModel):
    id: int = -1
    name: str = ""
    description: str = ""

    customer_type: int = -1
    business_status: int = -1


class WebSiteModel(BaseModel):
    id: int = -1
    name: str = ""
    description: str = ""
    domain: str
    type: int = -1

    school_id: str


class ModuleModel(BaseModel):
    id: int = -1
    name: str = ""
    description: str = ""

    website_id: str


class SubModuleModel(BaseModel):
    id: int = -1
    name: str = ""
    description: str = ""

    module_id: str


class PageModel(BaseModel):
    id: int = -1
    name: str = ""
    description: str = ""
    uri: str

    submodule_id: str


# endregion


# region shool crud
@router.get(path="/shool/list", summary="获取全部学校列表", description="格式：list[school]，")
async def get_all_school():
    with db_session:
        ret = School.select(is_delete=False)
        return [s.to_dict() for s in ret]


@router.get(path="/shool/", summary="通过id、名称查询学校信息", description="")
async def get_school_by_id(arg: str):
    with db_session:
        ret = select(ws for ws in School if ws.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in School if ws.name == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

    return {"code": 404, "msg": "查询不到符合条件的结果", "paras": arg}


#
# @router.get(path="/shool/name/", summary="通过名称查询学校信息", description="")
# async def get_school_by_name(name: str):
#     with db_session:
#         ret = School.select(name=name, is_delete=False)
#         return [s.to_dict() for s in ret]
#


@router.post(path="/shool/", summary="添加学校信息", description="")
async def add_school(args: SchoolModel):
    with db_session:
        ret = School.select(name=args.name)
        if ret.count() > 0:
            return {"code": 401, "msg": "学校名称已存在", "paras": str(args)}

        school = School(id=get_id())
        school.name = args.name
        school.description = args.description
        school.customer_type = args.customer_type
        school.business_status = args.business_status

        ret = {"code": 200, "msg": "已添加", "result": school.to_dict()}
        return ret


@router.delete(path="/shool/", summary="通过id删除学校信息", description="")
async def delete_school(id: str):
    with db_session:
        school = School.select(id=id)
        if school.count() <= 0:
            return {"code": 404, "msg": "目标对象不存在", "paras": id}

        for s in school:
            s.is_delete = True

        ret = {"code": 200, "msg": "已删除"}
        return ret


# endregion


# region website crud
@router.get(path="/website/list", summary="获取全部网站列表", description="")
async def get_all_ws():
    with db_session:
        ret = WebSite.select(is_delete=False)
        return [s.to_dict() for s in ret]


@router.get(path="/website/", summary="通过id、名称、domain、学校id 查询网站信息", description="")
async def get_ws_by_id(arg: str):
    with db_session:
        ret = select(ws for ws in WebSite if ws.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in WebSite if ws.name == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in WebSite if ws.domain == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(
            ws for ws in WebSite if ws.school.id == arg and ws.is_delete == False
        )
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

    return {"code": 404, "msg": "查询不到符合条件的结果", "paras": arg}


@router.post(path="/website/", summary="添加网站信息", description="")
async def add_school(args: WebSiteModel):
    with db_session:
        ret = WebSite.select(name=args.name)
        if ret.count() > 0:
            return {"code": 401, "msg": "网站名称已存在", "paras": str(args)}

        website = WebSite(id=get_id())
        website.name = args.name
        website.description = args.description
        website.domain = args.domain
        website.school = School.get(id=args.school_id)

        ret = {"code": 200, "msg": "已添加", "result": website.to_dict()}
        return ret


@router.delete(path="/website/", summary="通过id删除网站信息", description="")
async def delete_school(id: str):
    with db_session:
        ret = WebSite.select(id=id, is_delete=False)
        if ret.count() <= 0:
            return {"code": 404, "msg": "目标对象不存在", "paras": id}

        for s in ret:
            s.is_delete = True

        ret = {"code": 200, "msg": "已删除"}
        return ret


# endregion


# region module crud
@router.get(path="/module/list", summary="获取全部模块列表", description="")
async def get_all_mu():
    with db_session:
        ret = Module.select()
        return [s.to_dict() for s in ret]


@router.get(path="/module/", summary="通过id、名称、学校id 查询模块信息", description="")
async def get_mu_by_id(arg: str):
    with db_session:
        ret = select(ws for ws in Module if ws.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Module if ws.name == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Module if ws.web_site.school.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

    return {"code": 404, "msg": "查询不到符合条件的结果", "paras": arg}


@router.post(path="/module/", summary="添加模块信息", description="")
async def add_module(args: ModuleModel):
    with db_session:
        ret = select(
            r for r in Module if r.name == args.name and r.website.id == args.website_id
        )
        if ret.count() > 0:
            return {"code": 401, "msg": "网站模块名称已存在", "paras": str(args)}

        mu = Module(id=get_id())
        mu.name = args.name
        mu.description = args.description

        mu.web_site = WebSite.get(id=args.website_id)

        ret = {"code": 200, "msg": "已添加", "result": mu.to_dict()}
        return ret


@router.delete(path="/module/", summary="通过id删除模块信息", description="")
async def delete_module(id: str):
    with db_session:
        ret = Module.select(id=id, is_delete=False)
        if ret.count() <= 0:
            return {"code": 404, "msg": "目标对象不存在", "paras": id}

        for s in ret:
            s.is_delete = True

        ret = {"code": 200, "msg": "已删除"}
        return ret


# endregion


# region submodule crud
@router.get(path="/submodule/list", summary="获取全部子模块列表", description="")
async def get_all_mu():
    with db_session:
        ret = Submodule.select()
        return [s.to_dict() for s in ret]


@router.get(path="/submodule/", summary="通过id、名称、学校id 查询子模块信息", description="")
async def get_mu_by_id(arg: str):
    with db_session:
        ret = select(ws for ws in Submodule if ws.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Submodule if ws.name == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Submodule if ws.module.web_site.school.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

    return {"code": 404, "msg": "查询不到符合条件的结果", "paras": arg}


@router.post(path="/submodule/", summary="添加子模块信息", description="")
async def add_module(args: SubModuleModel):
    with db_session:
        ret = select(
            r
            for r in Submodule
            if r.name == args.name and r.module.id == args.module_id
        )
        if ret.count() > 0:
            return {"code": 401, "msg": "网站模块名称已存在", "paras": str(args)}

        mu = Submodule(id=get_id())
        mu.name = args.name
        mu.description = args.description

        mu.module = Module.get(id=args.module_id)

        ret = {"code": 200, "msg": "已添加", "result": mu.to_dict()}
        return ret


@router.delete(path="/submodule/", summary="通过id删除子模块信息", description="")
async def delete_module(id: str):
    with db_session:
        ret = Submodule.select(id=id, is_delete=False)
        if ret.count() <= 0:
            return {"code": 404, "msg": "目标对象不存在", "paras": id}

        for s in ret:
            s.is_delete = True

        ret = {"code": 200, "msg": "已删除"}
        return ret


# endregion


# region page crud
@router.get(path="/page/list", summary="获取全部页面列表", description="")
async def get_all_pg():
    with db_session:
        ret = Page.select()
        return [s.to_dict() for s in ret]


@router.get(path="/page/", summary="通过id、名称、学校id 查询页面信息", description="")
async def get_mu_by_id(arg: str):
    with db_session:
        ret = select(ws for ws in Page if ws.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Page if ws.name == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

        ret = select(ws for ws in Page if ws.submodule.module.web_site.school.id == arg)
        if len(ret[:]) > 0:
            return [s.to_dict() for s in ret]

    return {"code": 404, "msg": "查询不到符合条件的结果", "paras": arg}


@router.post(path="/page/", summary="添加页面信息", description="")
async def add_module(args: PageModel):
    with db_session:
        ret = select(
            r
            for r in Page
            if r.name == args.name and r.submodule.id == args.submodule_id
        )
        if ret.count() > 0:
            return {"code": 401, "msg": "名称已存在", "paras": str(args)}

        mu = Page(id=get_id())
        mu.name = args.name
        mu.description = args.description
        mu.uri = args.uri

        mu.pv = 0
        mu.uv = 0

        mu.submodule = Submodule.get(id=args.submodule_id)

        ret = {"code": 200, "msg": "已添加", "result": mu.to_dict()}
        return ret


@router.delete(path="/page/", summary="通过id删除页面信息", description="")
async def delete_module(id: str):
    with db_session:
        ret = Page.select(id=id, is_delete=False)
        if ret.count() <= 0:
            return {"code": 404, "msg": "目标对象不存在", "paras": id}

        for s in ret:
            s.is_delete = True

        ret = {"code": 200, "msg": "已删除"}
        return ret


# endregion
