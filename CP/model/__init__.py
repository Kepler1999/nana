from pony.orm import Database

db = Database()
db.bind(provider="sqlite", filename=r"C:\Users\liang\Desktop\Repo\common.sqlite",create_db=True)
# for test
# db.bind(provider="sqlite", filename=r":memory:", create_db=True)

# db.bind(provider="sqlite", filename=r"D:\Github\nana\common.sqlite", create_db=True)
