from pony.orm import db_session
from model import db

# Add Pony Models Here
from model.common import Country
from model.school_digitial_asset import School, WebSite, Module, Submodule, Page

db.generate_mapping(create_tables=True)
