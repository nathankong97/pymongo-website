'''THIS IS FOR THE CLASS INFO-I399 PYMONGO PROJECT TO THE WEB APPLICATION'''

from flask import Flask, redirect, url_for, request
from flask_pymongo import PyMongo
import pymongo
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'tester'
app.config['MONGO_URI'] = 'mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester'

mongo = PyMongo(app)

consultant = mongo.db.consultant
company = mongo.db.companies
assignment = mongo.db.assignment

@app.route('/')
def start():
    html = '''<!doctype html>
<html>
  	<head>
      <meta charset="utf-8">
      <title>INFO-I399</title>
  	</head>
  	<body>
      <h1>PyMongo Homework</h1>
      <p><b>Show Collections</b></p>
      <form action="http://127.0.0.1:5000/show_col" method="post">
        	<button type="submit", name = 'action' value = 'con'>Consultant</button>
        	<button type="submit", name = 'action' value = 'com'>Company</button>
        	<button type="submit", name = 'action' value = 'ass'>Assignment</button>
      </form>
      <br>
      <p><b>Query 1: Count accountants based on fields</b></p>
      <p>example type: gender, expertise, skill_level, home_town, on_line</p>
      <form action="http://127.0.0.1:5000/agg" method="post">
      <p><input type = 'text' name = 'field'/></p>
      <p><button type="submit" value = 'count'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/insert" method="post">
      <p><b>Query 2: Insert value to the Assignment</b></p>
      <p>Consultant ID <input type = 'text' name = 'con'/></p>
      <p>Company ID <input type = 'text' name = 'com'/></p>
      <p>Hour <input type = 'text' name = 'hour'/></p>
      <p>Date Completed <input type = 'text' name = 'date'/>(format:m/d/yyyy)</p>
      <p>Rating <input type = 'text' name = 'rate'/>(1-5)</p>
      <p><button type="submit" value = 'insert'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/display" method="post">
      <p><b>Query 3: Display consultants based on expertise </b></p>
      <p>Please enter an expertise (Neo4j, Cassandra, Redis, MongoDB) so we can display consultants accordingly.</p>
      <p><input type = 'text' name = 'expertise'/></p>
      <p><button type="submit" value = 'display'>Submit</button>
      </form>
      <br>
      <form action="/company" method="post">
      <p><b>Query 4: Display all consultants in a chosen company</b></p>
      <p>Please select a company'name from following(Brightdog,Oba,Realcube,Zoomcast,Devify,Aimbo,Dynazzy,Eimbee,Yacero,Oyoloo):</p>
      <p><input type = 'text' name = 'company'/></p>
      <p><button type="submit" value = 'display'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/date" method="post">
      <p><b>Query 5: Display consultants and assignment based on date</b></p>
      <p>Please enter a date (m/dd/yyyy) and we will display each consultant and how many assignments they completed.</p>
      <p><input type = 'text' name = 'date_com'/></p>
      <p><button type="submit" value = 'date'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/hometown" method="post">
      <p><b>Query 6: Display consultants from a chosen home town</b></p>
      <p>Please select a hometown (Indianapolis, Bloomington, Chicago) and we will display consultants from there.</p>
      <p><input type = 'text' name = 'home'/></p>
      <p><button type="submit" value = 'home'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/fee" method="post">
      <p><b>Query 7: Choose High fee(greater than or equal to 150) or Low fee(less than 150) and display appropriate consultants</b></p>
      <p>Please select a High or Low and we will display consultants based on their fee.</p>
      <p><input type = 'text' name = 'fee'/></p>
      <p><button type="submit" value = 'fee'>Submit</button>
      </form>
      <br>
      <form action="http://127.0.0.1:5000/rating" method="post">
      <p><b>Query 8: Display the consultant_ID, first name, last name, and average rating for every consultant</b></p>
      <p><button type="submit" value = 'rating'>Submit</button>
      </form>
  </body>
  
</html>'''
    return html

def read_col(col):
    mydoc = col.find({})
    return mydoc

def table(col):
    content = "<table style='width:100%' border = '1'><tr>"
    for i in list(col[0].keys())[1:]:
        content += '<th>' + str(i) + '</th>'
    content += '</tr>'
    for i in col:
        content += '<tr>'
        for x in list(i.values())[1:]:
            content += '<td>' + str(x) + '</td>'
        content += '</tr>'
    content += '</table>'
    return content

'''Show collections'''
@app.route('/show_col', methods = ['POST'])
def show_col():
    html = '''<!doctype html>
<html>
  	<head>
      <meta charset="utf-8">
      <title>INFO-I399</title>
  	</head>
  	<body>
      <h1>Show collection</h1>
      {content}
  </body>
</html>'''

    if request.form['action'] == 'con':
        mydoc = read_col(consultant)
    elif request.form['action'] == 'com':
        mydoc = read_col(company)
    elif request.form['action'] == 'ass':
        mydoc = read_col(assignment)
    content = table(mydoc)
    return html.format(content = content)

'''query 1'''
@app.route('/agg', methods = ['POST'])
def agg():
    html = '''<!doctype html>
    <html>
      	<head>
          <meta charset="utf-8">
          <title>INFO-I399</title>
      	</head>
      	<body>
          <h1>Aggregation Count</h1>
          {content}
      </body>
    </html>'''
    content = ''
    text = request.form['field']
    if text == '':
        mydoc = consultant.find({}).count()
        content += '<p>The total Consultant is: ' + str(mydoc) + '</p>'
        return html.format(content=content)
    query = [{'$group': {'_id': '$'+ text, 'count': {'$sum': 1}}}]
    mydoc = consultant.aggregate(query)

    for i in mydoc:
        content += str(i) + '<br>'
    return html.format(content=content)

'''query 2'''
@app.route('/insert', methods = ['POST'])
def insert():
    con = request.form['con']
    com = request.form['com']
    hour = request.form['hour']
    date = request.form['date']
    rate = request.form['rate']
    if (con or com or hour or date or rate) == '':
        return '<p>You need to fulfill all fields</p>'
    mydict = {'company_ID':int(con),'consultant_ID':int(com),'hours':int(hour),'date_completed':date,'rating':int(rate)}
    x = assignment.insert_one(mydict)
    return '<br><p>Insert Complete</p>'

'''query 3'''
@app.route('/display', methods = ['POST'])
def expertise():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    myclient = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    html = '''<!doctype html>
        <html>
          	<head>
              <meta charset="utf-8">
              <title>INFO-I399</title>
          	</head>
          	<body>
              <h1>Result</h1>
              {content}
          </body>
        </html>'''
    content = ''
    mydb = myclient.get_database('tester')
    mycol = mydb["consultant"]

    text = request.form['expertise']

    expertise = {"expertise": text}
    exp_results = mycol.find(expertise)
    content += table(exp_results)
    return html.format(content = content)

'''query 4'''
@app.route('/company', methods = ['POST'])
def company():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    db = client.get_database('tester')
    assignment = db.assignment
    html = '''<!doctype html>
                    <html>
                      	<head>
                          <meta charset="utf-8">
                          <title>INFO-I399</title>
                      	</head>
                      	<body>
                          <h1>Consultants</h1>
                          {content}
                      </body>
                    </html>'''
    content = ''
    text = request.form['company']
    query = ([
        {'$lookup': {
            'from': 'consultant',
            'localField': 'consultant_ID',
            'foreignField': 'id',
            'as': 'consultant_info'}},
        {'$unwind': '$consultant_info'},
        {'$lookup': {
            'from': 'companies',
            'localField': 'company_ID',
            'foreignField': 'id',
            'as': 'company_info'}},
        {'$unwind': '$company_info'},
        {'$project': {
            'company_info.company_name': 1,
            'consultant_info.first_name': 1,
            'consultant_info.last_name': 1,
            'consultant_info.email': 1,
            'consultant_info.gender': 1,
            'consultant_info.hourly_fee': 1,
            'consultant_info.expertise': 1,
            'consultant_info.home_town': 1,
            'consultant_info.skill_level': 1,
            'consultant_info.on_line': 1
        }}]);

    jointable = assignment.aggregate(query)
    count = 0
    content += "<table style='width:100%' border = '1'>"
    for i in jointable:
        if i["company_info"]["company_name"] == text:
            count+= len(i)
            content += '<tr>'
            for x in i["consultant_info"].values():
                content += '<td>' + str(x) + '</td>'
            content += '</tr>'
    content += '</table>'

    return html.format(content = content)

'''query 5'''
@app.route('/date', methods = ['POST'])
def date():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    myclient = MongoClient(MONGODB_URI, connectTimeoutMS=30000)

    mydb = myclient.get_database('tester')
    mycol = mydb["assignment"]

    html = '''<!doctype html>
            <html>
              	<head>
                  <meta charset="utf-8">
                  <title>INFO-I399</title>
              	</head>
              	<body>
                  <h1>Result</h1>
                  {content}
              </body>
            </html>'''
    content = ''
    text = request.form['date_com']
    try:
        date = {"date_completed": text}
        date_results = mycol.find(date)
        consultant_count = {}

        for x in date_results:
            if x["consultant_ID"] in consultant_count.keys():
                c_id = x["consultant_ID"]
                temp = consultant_count[c_id]
                temp += 1
                consultant_count[c_id] = temp
            else:
                c_id = x["consultant_ID"]
                consultant_count[c_id] = 1

        concol = mydb["consultant"]
        results = []

        for item in consultant_count.keys():
            result_lst = []

            consultant = {"id": item}
            cons_results = concol.find(consultant)

            for y in cons_results:
                result_lst.append(item)
                result_lst.append(y['first_name'])
                result_lst.append(y['last_name'])
                result_lst.append(consultant_count[item])
            results.append(result_lst)
        content += "<table border = '1'><tr><th>Consultant ID</th><th>First Name</th><th>Last Name</th><th>Number</th><tr>"
        for i in results:
            content += '<tr>'
            for x in i:
                content += "<td>" + str(x) + "</td>"
            content += '</tr>'
        content += "</table>"
        return html.format(content = content)
    except:
        content += '<p>Empty Set</p>'
        return html.format(content = content)

'''query 6'''
@app.route('/hometown', methods = ['POST'])
def home():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    myclient = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    html = '''<!doctype html>
            <html>
              	<head>
                  <meta charset="utf-8">
                  <title>INFO-I399</title>
              	</head>
              	<body>
                  <h1>Result</h1>
                  {content}
              </body>
            </html>'''
    content = ''
    text = request.form['home']
    mydb = myclient.get_database('tester')
    mycol = mydb["consultant"]
    hometown = {"home_town": text.title()}
    ht_results = mycol.find(hometown)
    content += table(ht_results)
    return html.format(content = content)

'''query 7'''
@app.route('/fee', methods = ['POST'])
def fee():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    myclient = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    html = '''<!doctype html>
                <html>
                  	<head>
                      <meta charset="utf-8">
                      <title>INFO-I399</title>
                  	</head>
                  	<body>
                      <h1>Result</h1>
                      {content}
                  </body>
                </html>'''
    content = ''
    text = request.form['fee']
    if text.lower() == 'high':
        fee = {'hourly_fee': {'$gte': 150}}
    else:
        fee = {'hourly_fee': {'$lt': 150}}
    mydb = myclient.get_database('tester')
    mycol = mydb["consultant"]

    fee_results = mycol.find(fee)
    content += table(fee_results)
    return html.format(content = content)

'''query 8'''
@app.route('/rating', methods = ['POST'])
def rate():
    from pymongo import MongoClient
    MONGODB_URI = "mongodb://test:q1w2e3@ds229771.mlab.com:29771/tester"
    client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
    html = '''<!doctype html>
                    <html>
                      	<head>
                          <meta charset="utf-8">
                          <title>INFO-I399</title>
                      	</head>
                      	<body>
                          <h1>Consultant Average Rating</h1>
                          {content}
                      </body>
                    </html>'''
    content = ''
    mydb = client.get_database('tester')
    mycol = mydb["assignment"]

    average_ratings = mycol.aggregate([{'$group': {'_id': '$consultant_ID', 'average_rating': {'$avg': '$rating'}}}])

    consultant_rating = {}

    for item in average_ratings:
        c_id = item['_id']
        c_rating = item['average_rating']
        consultant_rating[c_id] = c_rating

    concol = mydb["consultant"]
    results = []

    for item in consultant_rating.keys():
        result_lst = []

        consultant = {"id": item}
        cons_results = concol.find(consultant)

        for y in cons_results:
            result_lst.append(item)
            result_lst.append(y['first_name'])
            result_lst.append(y['last_name'])
            result_lst.append(consultant_rating[item])

        results.append(result_lst)
    content += "<table border = '1'><tr><th>Consultant ID</th><th>First Name</th><th>Last Name</th><th>Average Rating</th><tr>"
    for i in results:
        content += '<tr>'
        for x in i:
            content += '<td>' + str(x) + '</td>'
        content += '</tr>'
    content += '</table>'
    return html.format(content = content)

if __name__ == '__main__':
    app.run(debug=True)

