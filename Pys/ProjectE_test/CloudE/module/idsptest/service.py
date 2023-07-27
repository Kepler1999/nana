from flask import Flask
from saver import db, Modular,Item,Page,IdspView,IdspSchool,func_exec_time
from pony.orm import *

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@func_exec_time
@app.route('/school/')
def get_all_schools():
    ret = []
    with db_session:
        s = select(s for s in IdspSchool)[:]
        for i in s:
            ret.append(i.to_dict())
    return ret

@func_exec_time
@app.route('/school/<name>')
def getSchool(name):
    if name == None:
        return 'Need school name or identity'
    
    ret = []
    with db_session:
        s = select(s for s in IdspSchool)[:]
        for i in s:
            ret.append(i.to_dict())
    return ret



if __name__ == '__main__':
    db.generate_mapping()
    app.run(debug=True)