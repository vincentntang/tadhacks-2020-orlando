from flask import Flask, request, redirect, session, url_for, Response, json
from flask.json import jsonify

import json
import os
import random
##from twilio.rest import Client
import time
import requests
from pymongo import MongoClient
from pprint import pprint
import math
from flask_cors import CORS

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)



client = MongoClient("mongodb+srv://rootzero:fitx@cluster0-jnzul.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = client["tadhack2020"]


lat = 29.486458
lon = -81.207935



def updateLatLonUser(lat, lon, userid):
    col = db.users
    col.update_one({"name":str(userid)}, {"$set":{"lat":str(lat)}})
    col.update_one({"name":str(userid)}, {"$set":{"lon":str(lon)}})
    



def add2area(areaname, userid):
    col = db.buildings
    area  = col.find_one({"code": str(areaname)})
    oldpop = int(area["pop"])
    newpop = oldpop+1
    col.update_one({"code":str(areaname)}, {"$set":{"pop":str(newpop)}})
    col = db.users
    col.update_one({"name":str(userid)}, {"$set":{"lastlocation":str(areaname)}})

def removefromarea(areaname, userid):
    col = db.buildings
    area  = col.find_one({"code": str(areaname)})
    oldpop = int(area["pop"])
    newpop = max([oldpop-1,0])
    col.update_one({"areaname":str(areaname)}, {"$set":{"pop":str(newpop)}})
    col = db.users
    col.update_one({"name":str(userid)}, {"$set":{"lastlocation":"unknown"}})



@app.route("/getPopulationByArea", methods=['GET', 'POST'])
def getpopulationbyarea():

    # print(request)

    res = request.get_json()
    print (res)

    aname = res["areaname"]
    col = db.buildings
    user = col.find_one({"code": str(res["areaname"])})

    payload = {}

    payload["population"] = user["pop"]
         


    print(payload)
    
    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["data"] = payload 

    statusjson = json.dumps(status)

    # print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp







@app.route("/getAllUsers", methods=['GET', 'POST'])
def getallusers():

    # print(request)

    res = request.get_json()
    print (res)

    # tag = res["tag"]
    col = db.users
    users = col.find()

    
    payload = {}
    u = []

    for user in users:
        user = JSONEncoder().encode(user)
        u.append(user)
    # u = jsonify(u)
    payload["users"] = u
    

    print(payload)
    
    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["data"] = u

    statusjson = json.dumps(status)

    # print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


@app.route("/getAllEvents", methods=['GET', 'POST'])
def getallevents():

    # print(request)

    res = request.get_json()
    print (res)

    # tag = res["tag"]
    col = db.events
    events = col.find()

    
    payload = {}
    u = []

    for event in events:
        event = JSONEncoder().encode(event)
        u.append(event)
    # u = jsonify(u)
    payload["events"] = u
    

    print(payload)
    
    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["data"] = u

    statusjson = json.dumps(status)

    # print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp





@app.route("/addUser", methods=['GET', 'POST'])
def addUser():

    # print(request)

    res = request.get_json()
    print (res)

    ts = str(int(time.time()))

    col = db.users

    
    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["request"] = res 

    statusjson = json.dumps(status)

    # print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp



@app.route("/getStats", methods=['GET', 'POST'])
def getStats():

    # print(request)

    res = request.get_json()
    print (res)

    text = res["message"]
    text = text.split(",")
    county = text[0]
    state = text[1]

    col = db.usa_current
    curr_cases = 0
    curr_deaths = 0
    pred_cases = 0
    # pred_deaths = 0
    place = state+county

    result = col.find({"Region":state,"County":county}).sort([('Days Since 2019-12-31',-1)]).limit(1)
    for r in result:
        print (r)
        curr_deaths = r["Deaths"]
        curr_cases = r["Confirmed"]
    
    col = db.usa_predicted
    result = col.find({"place":place}).sort([('predicted_Confirmed',-1)]).limit(1)
    for r in result:
        print (r)
        # pred_deaths = r["Deaths"]
        pred_cases = math.ceil(float(r["predicted_Confirmed"]))



    resraw = request.get_data()
    # print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()
 

    status = {}
    # status["server"] = "up"
    # status["message"] = "some random message here"
    # status["request"] = res 
    status["state"] = state 
    status["county"] = county 
    status["Cases_so_far"] = curr_cases 
    status["Deaths_so_far"] = curr_deaths 
    status["Predicted_Cases_30_days_later"] = str(pred_cases) 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp



@app.route("/dummyJson", methods=['GET', 'POST'])
def dummyJson():

    # print(request)

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    # print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()
 

    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp
    




@app.route("/dummy", methods=['GET', 'POST'])
def dummy():

    ##res = request.json

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp



if __name__ == "__main__":
    # app.run(debug=True, host = 'localhost', port = 8002) ##server settings here  HOLLA
    # app.run(debug=True, host = '52.116.36.178', port = 8001)
    # app.run(debug=True, host = '35.238.165.103', port = 8001)
    app.run(debug=True, host = '45.79.199.42', port = 8002)