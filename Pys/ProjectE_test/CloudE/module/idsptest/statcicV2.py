import sys,os
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pony.orm import *
from tools import func_exec_time

db = Database() 
db.bind(provider="sqlite", filename=r"C:\Users\liang\Desktop\Repo\idsp_opdata2.sqlite",create_db=True)

# region models

class School(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    web_sites = Set('WebSite')
    type = Optional(int)


class WebSite(db.Entity):
    id = PrimaryKey(int, auto=True)
    domain = Optional(str)
    school = Optional(School)
    modules = Set('Module')


class Module(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    web_site = Required(WebSite)
    submodules = Set('Submodule')


class Submodule(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    module = Required(Module)
    pages = Set('Page')


class Page(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    submodule = Required(Submodule)
    pv = Optional(int)
    uv = Optional(int)

# endregion models

# region save data
@func_exec_time
@db_session
def save():
    # save school and website
    School_file_path = r"C:\Users\liang\Desktop\Repo\IDSP-BOSS 学校列表.xlsx"
    import pandas as pd
    df = pd.read_excel(School_file_path)
    
    for i in tqdm(df.index):
        name = str(df.loc[i, "名称"])
        domain = str(df.loc[i, "域名"])
        teacher_num = str(df.loc[i, "教师人数"])
        student_num = str(df.loc[i, "学生人数"])   
        parenet_num = str(df.loc[i, "家长人数"])   
        
        if len(name)<1 or len(domain)<1 or School.get(name=name):
            continue
        
        school = School()
        school.name = name
        
        website = WebSite()
        website.domain = domain
        website.school = school
        
        
    # save module and page data

    df = pd.read_csv(r"C:\Users\liang\Desktop\Repo\idsp_sitemap.csv")
    "模块 菜单 页面 Uri"
    for i in tqdm(df.index):
        modular_name = str(df.loc[i, "模块"])
        item_name = str(df.loc[i, "菜单"])
        pass_name = str(df.loc[i, "页面"])
        uri = str(df.loc[i, "Uri"])        
        
        # uri format
        uri = uri.replace("src=","").replace('"','')
        
        if modular_name.lower() == "nan":
            for j in range(i-1,-1,-1):
                modular_name = str(df.loc[j, "模块"])
                if modular_name.lower()!= "nan":
                    break
                
        if item_name.lower() == "nan":
            for j in range(i-1,-1,-1):
                item_name = str(df.loc[j, "菜单"])                
                if item_name.lower()!= "nan":
                    break
    
        # create model object
        module = Module.get(name=modular_name)
        if module is None:
            module = Module(name=modular_name)
            commit()
        
        submodule = Submodule.get(name=item_name)
        if submodule is None:
            submodule = Submodule(name=item_name,module=module)
            commit()
        
        page = Page.get(name=pass_name,uri=uri)
        if page is None:
            page = Page(name=pass_name,uri=uri,item=item)
            commit()

# endregion 

# region statistics
@func_exec_time
@db_session
def static():
    pass
# endregion statistics

if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    save()
    static()