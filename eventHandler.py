#! /usr/bin/python3

from os import path
import json
import requests

def save_data_to_file(honeypotEvent, service):
    jsonLayer = []
    jsonFile = {}

    if service == 'HTTP':
        filename = './http_log.json'
    if service == 'VSFTPD':
        filename = './vsftpd_log.json'
    
    with open(filename) as fp:
        jsonFile = json.load(fp)
        jsonFile.append(honeypotEvent)

    with open(filename, 'w') as json_file:
        json.dump(jsonFile, json_file, indent = 4, separators = (',',': '))

    print("New Request saved")

def json_format_API(timestamp, types, content):
    honeypotEvent = {}
    event = {}
    event["honeypotID"] = 1 
    event["token"] = "44a0f077ee35dc76b213ee45c33b88d97d3c27cb49c458720f47892302d1e76f"
    event["timestamp"] = timestamp
    event["type"] = types
    event["content"] = content
    honeypotEvent["event"] = event

    print(honeypotEvent)

    if types == "login":
        save_data_to_file(honeypotEvent, content.get('service'))

    send_request_to_API(honeypotEvent)

def send_request_to_API(honeypotEvent):
    
    rqst = requests.post('https://seclab.fiw.fhws.de/input/', json=honeypotEvent)
    print(rqst.status_code, rqst.reason)

