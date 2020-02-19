from SetupDb import db_session
import SetupDb
from Model import Interview
import datetime
import datetime
from datetime import datetime
from datetime import datetime, timedelta
from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify
import json

app = Flask(__name__)

SetupDb.init_db()
# dummyInterviewdata = Interview(2,2,"F2F", "Niyuj HQ", "NA", "NA", datetime.datetime.now())
#
# db_session.add(dummyInterviewdata)
# db_session.commit()




@app.route('/interviews')
def get_interviews():
    interviews = db_session.query(Interview).all()
    interview_list = []
    for interview in interviews:
        interview_list.append(interview.serialize())
    return jsonify(interview_list)

@app.route('/interviews/<id>')
def get_interview(id):
    return jsonify(db_session.query(Interview).get(id).serialize())

@app.route('/interviews/candidate/<id>')
def get_interview_by_candidate_id(id):
    result = db_session.query(Interview).filter(Interview.job_has_candidate_id == id)
    candidate_list = []
    for value in result:
        candidate_list.append(value.serialize())
    return jsonify(candidate_list)


@app.route('/interviews/days/<days>')
def get_interview_by_date(days):
    current_date = datetime.now()
    search_date = datetime.now() + timedelta(days=int(days))
    results = db_session.query(Interview).filter(Interview.schedule_time.between(current_date, search_date))
    date_list = []
    for value in results:
        date_list.append(value.serialize())
    return jsonify(date_list)


@app.route('/interviews/<id>', methods = ['DELETE'])
def delete_interview(id):
    x = db_session.query(Interview).get(id)
    db_session.delete(x)
    db_session.commit()
    return {"status": "OK"}

@app.route('/interviews/schedule', methods = ['POST'])
def post_interview():
   content = request.get_json()
   interviewObj = Interview(content)
   db_session.add(interviewObj)
   db_session.commit()
   return {"id": interviewObj.id,"status": "OK"}

@app.route('/interviews/schedule/<id>', methods = ['PUT'])
def update_interview(id):
   content = request.get_json()
   interviewUpdatedObj = Interview(content)
   # interviewObj.id = id
   # db_session.add(interviewObj)
   interviewObj = db_session.query(Interview).get(id)
   interviewObj = interviewUpdatedObj
   db_session.commit()
   return {"id": interviewObj.id,"status": "OK"}


if __name__ == '__main__':
   app.run(debug = True)
