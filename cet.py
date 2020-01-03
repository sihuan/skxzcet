from flask import Flask
from pdf import parse_number_from_content
import requests

app = Flask(__name__)


@app.route('/cet/<sid>/')
def code(sid):
    try:
        session = requests.Session()
        req = session.get(
            "http://cet-bm.neea.edu.cn/Home/DownTestTicket?SID="+str(sid))
        exam, school, number = parse_number_from_content(req.content)
        data = {
            "status": 0,
            "exam": exam,
            "school": school,
            "number": number
        }
    except:
        data = {
            "status": -1,
            "exam": "🐱",
            "school": "🐶",
            "number": "🐭"
        }
    return data


app.run(host='0.0.0.0', port=8008)
