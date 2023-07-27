from pony.orm import Database

db = Database() 
db.bind(provider="sqlite", filename=r"C:\Users\liang\Desktop\Repo\common.sqlite",create_db=True)