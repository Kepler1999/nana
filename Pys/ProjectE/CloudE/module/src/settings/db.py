from pony.orm import Database

db = Database() 
db.bind(provider="sqlite", filename=":memory:",create_db=True)