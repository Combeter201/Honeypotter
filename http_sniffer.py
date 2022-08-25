#! /usr/bin/python3

from scapy.all import *
print("Sniffing ...")

sniff(filter="tcp port 21", prn=lambda x: x.sprintf('%Raw.load%'))
