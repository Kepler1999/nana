from saver import db, Modular,Item,Page,IdspView,IdspSchool,func_exec_time
from pony.orm import *
from tqdm import tqdm

# page view check
@func_exec_time
@db_session
def statics():
    
    # static page pv/uv
    pages = Page.select()
    
    for i in tqdm(pages[:]):
        
        page_pv = select(p for p in IdspView if i.uri in p.URL)
        
        pv = sum([int(x.PV) for x in page_pv])        
        i.pv = pv
        
        uv = sum([int(x.UV) for x in page_pv])
        i.uv = uv
        
        rollout = sum([int(x.Rollout) for x in page_pv])
        i.rollout = rollout
        
        contribute = sum([int(x.Contribute) for x in page_pv])
        i.contribute = contribute

    commit()
    
    # static item pv/uv
    items = Item.select()
    
    for i in tqdm(items[:]):
        
        i_p = select(p for p in Page if p.item == i)
        
        i.pv = select(p.pv for p in i_p).sum()
        i.uv = select(p.uv for p in i_p).sum()
        
    commit()
    # static modular pv/uv
    modulars = Modular.select()
    
    for m in tqdm(modulars[:]):
        m_i = select(i for i in Item if i.modular == m)
        
        m.pv = select(i.pv for i in m_i).sum()
        m.uv = select(i.uv for i in m_i).sum()
    
    commit()

@func_exec_time
@db_session
def statics_school():
    school = IdspSchool.select()
    for s in tqdm(school[:]):
        
        pg_view = select(v for v in IdspView if s.domain in v.URL)
        
        pv = select(int(i.PV) for i in pg_view).sum()
        uv = select(int(i.UV) for i in pg_view).sum()

        s.pv = pv
        s.uv = uv
    

if __name__ == '__main__':
    db.generate_mapping()
    statics_school()
    