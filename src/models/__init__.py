from pony.orm import Database

db = Database()
# db.bind(provider="sqlite", filename=r"C:\Users\liang\Desktop\Repo\common.sqlite",create_db=True)
# db.bind(provider="sqlite", filename=":memory:",create_db=True)

db.bind(provider="sqlite", filename="common.sqlite", create_db=True)
