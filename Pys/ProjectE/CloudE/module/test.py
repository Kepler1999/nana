from models._db import db
from models.common import Country

from typing import List
from pony.orm import *

from tools import func_exec_time


@func_exec_time
@db_session
def save_country(country:List[dict]):
    for x in country:
        if select(c for c in Country if c.name_chs ==  x['name_chs']).count() > 0:
            print("ignoring")
            continue
            
        c = Country(
            name_chs = x['name_chs'],
            name_eng = x['name_eng'],
            fullname_eng = x['fullname_eng'],
            alphabet_code_2 = x['alphabet_code_2'],
            alphabet_code_3 = x['alphabet_code_3'],
        )



if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    
    import pandas as pd
    df = pd.read_csv(r"C:\Users\liang\Desktop\Repo\country.csv")
    
    # print(df.head(5))
    
    data = []
    for i in df.index:
        name_chs = df.loc[i,"中文简称"] 
        name_eng = df.loc[i,"英文简称"]
        fullname_eng = df.loc[i,"英文全称"]
        alphabet_code_2 = df.loc[i,"两字母代码"]
        alphabet_code_3 = df.loc[i,"三字母代码"]
        
        if name_chs is None  or str(name_chs).lower() == "nan":
            continue
        
        d = {
            "name_chs": str(name_chs),
            "name_eng": str(name_eng),
            "fullname_eng": str(fullname_eng),
            "alphabet_code_2": str(alphabet_code_2),
            "alphabet_code_3": str(alphabet_code_3),
        }
        
        data.append(d)
        
    save_country(data)
        
    ################################################################
    with db_session:
        count = select(c for c in Country)
        
        for c in count:
            print(c.name_chs, c.name_eng, c.fullname_eng, c.alphabet_code_2, c.alphabet_code_3)