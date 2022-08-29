#! /usr/bin/python3

from flask import Flask, request, render_template
from os import path
from eventHandler import *
import datetime
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":

        content = {}
        content["srcIP"] = request.remote_addr
        content["service"] = "HTTP"
        content["user"] = request.form["username"]
        content["pass"] = request.form["password"]

        json_format_API(
                (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                "login",
                content)
#                request.headers.get("User-Agent"))

    if request.method == "GET":

        content = {}
        content["srcIP"] = request.remote_addr
        content["requestType"] = "GET"
        content["requestString"] = request.path
        content["agent"] = request.headers.get("User-Agent")

        json_format_API(
                (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                "HTTP",
                content)
#                request.headers.get("User-Agent")

    return render_template('login.html')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
