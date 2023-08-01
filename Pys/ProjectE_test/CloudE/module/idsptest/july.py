from saver import db, Modular,Item,Page,IdspView,IdspSchool,SchoolPageView
from pony.orm import *
from tqdm import tqdm


# static shcool 

@db_session
def schools_be_visited():
    urls = select(i.URL for i in IdspView)
    urls = [u.replace("https://","") for u in urls]
    urls = [u.replace("http://","") for u in urls]
    domains = [u.split("/")[0] for u in urls]
    domains = set(domains)
    return list(domains)

@db_session
def schools_page_static():
    schools_domain = schools_be_visited()
    page = Page.select()

    school_views = IdspView.select()

    for school in tqdm(schools_domain):
        for p in page[:]:

            sp = SchoolPageView()

            sp.school_id = school
            sp.page_id = p.id

            pv = select(int(s.PV) for s in IdspView if str(sp.school_id) in s.URL and str(sp.page_id) in s.URL).sum()
            uv = select(int(s.UV) for s in IdspView if str(sp.school_id) in s.URL and str(sp.page_id) in s.URL).sum()

            sp.pv = pv
            sp.uv = uv

@db_session
def static_school_view():
    ret = SchoolPageView.select()


if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    # [print(x) for x in schools_be_visited()]
    # schools_page_static()
    static_school_view()
