import sys,os
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pony.orm import *
from tools import func_exec_time

db = Database() 
db.bind(provider="sqlite", filename=r"C:\Users\liang\Desktop\Repo\idsp_opdata.sqlite",create_db=True)

# region idsp_sitemap model

class Modular(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    
    pv = Optional(int)
    uv = Optional(int)
        
    item = Set(lambda:Item)

class Item(db.Entity):
    modular = Required(Modular,reverse="item")
    
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    
    pv = Optional(int)
    uv = Optional(int)
    
    page = Set(lambda:Page)

class Page(db.Entity):
    item = Required(Item,reverse="page")
    
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    uri = Required(str)
    description = Optional(str)
    
    pv = Optional(int)
    uv = Optional(int)
    duration = Optional(str)
    rollout = Optional(int)
    contribute = Optional(int)

# endregion

# region school domain

class IdspSchool(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    domain = Required(str)
    teacher_num = Optional(int)
    student_num = Optional(int)
    parent_num = Optional(int)

# endregion

# region idspview models
class IdspView(db.Entity):
    URL = Required(str)
    PV = Required(str)
    UV = Required(str)
    Contribute = Required(str)
    Rollout = Required(str)
    Duration = Required(str)
    
# endregion 
@func_exec_time
@db_session
def save_from_csv():
    import pandas as pd
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
        modular = Modular.get(name=modular_name)
        if modular is None:
            modular = Modular(name=modular_name)
            commit()
        
        item = Item.get(name=item_name)
        if item is None:
            item = Item(name=item_name,modular=modular)
            commit()
        
        page = Page.get(name=pass_name,uri=uri)
        if page is None:
            page = Page(name=pass_name,uri=uri,item=item)
            commit()


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    save_from_csv()