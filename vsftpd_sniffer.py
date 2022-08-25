#! /usr/bin/python3

import json
import datetime
from os import path
from scapy.all import *
print("Sniffing ...")

filename = './vsftpd_login.json'
jsonObj = []
newlogin = {}

def save_data_to_json(input):
    global jsonObj
    global newlogin
    with open(filename) as fp:
        jsonObj = json.load(fp)

        if "uploaded_file" not in input:
            jsonObj.append(input)
        else:
            jsonObj.append(input)

    with open(filename, 'w') as json_file:
        json.dump(jsonObj, json_file, indent = 4, separators = (',',': '))
    
    newlogin = {}
    jsonObj = []
    if "uploaded_file" in input:
        newlogin_with_file = {}

def ftp_informations(packet):
    src = packet.getlayer(IP).src
    dest = packet.getlayer(IP).dst
    raw = packet.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)', raw)
    passwd = re.findall('(?i)PASS (.*)', raw)
    data = re.findall('(?i)STOR (.*)', raw)

    if user:
        global newlogin
        newlogin['timestamp'] = (datetime.now()).strftime("%c")
        newlogin['src_ip'] = str(src)
        newlogin['user'] = str(user[0]).replace("\\r\\n'", "")

    if passwd:
        newlogin['password'] = str(passwd[0]).replace("\\r\\n'", "")

    if data:
        global newlogin_with_file
        newlogin = newlogin_with_file
        newlogin['uploaded_file'] = str(data[0]).replace("\\r\\n'", "")
    
    if "user" in newlogin and "password" in newlogin:
        if "uploaded_file" in newlogin:
            save_data_to_json(newlogin)
        else:
            newlogin_with_file = newlogin
            save_data_to_json(newlogin)

sniff(filter='tcp port 21', prn=ftp_informations)
