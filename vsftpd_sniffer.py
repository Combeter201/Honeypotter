#! /usr/bin/python3

import json
import datetime
from os import path
from scapy.all import *
from eventHandler import *
print("Sniffing ...")

filename = './vsftpd_log.json'
jsonObj = []
content = {}

def ftp_informations(packet):
    src = packet.getlayer(IP).src
    dest = packet.getlayer(IP).dst
    raw = packet.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)', raw)
    passwd = re.findall('(?i)PASS (.*)', raw)
    data = re.findall('(?i)STOR (.*)', raw)


    if user:
        global content
        content["srcIP"] = src
        content["service"] = "VSFTPD"
        content["user"] = str(user[0]).replace("\\r\\n'", "")

    if passwd:
        content["pass"] = str(passwd[0]).replace("\\r\\n'", "")

    if data:
        global content_with_file
        content = content_with_file
        content['uploaded_file'] = str(data[0]).replace("\\r\\n'", "")

    if "user" in content and "pass" in content:
        if "uploaded_file" in content:
            json_format_API(
                    (datetime.now()).strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                    "vsftpd_fileupload",
                    content)
            content = {}
            content_with_file = {}

        else:
            content_with_file = content
            json_format_API(
                    (datetime.now()).strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
                    "login",
                    content)
            content = {}


sniff(filter='tcp port 21', prn=ftp_informations)
