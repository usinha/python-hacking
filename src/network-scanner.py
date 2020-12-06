#!/usr/bin/env python3
import scapy.all as scapy
import argparse
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",help="Target IP/IP Range")
    options= parser.parse_args()
    return options
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    #print(arp_request.show())
    broadcast = scapy.Ether(dst=("ff:ff:ff:ff:ff:ff"))  # ether packket required to broadcast
    arp_request_broadcast = broadcast/arp_request
    #print(arp_request_broadcast.summary())
    #print(arp_request_broadcast.show())
    #
    ans,unans = scapy.srp(arp_request_broadcast,timeout=1,verbose=False) # returns list of answers,unanswered
    #print(len(ans))
    #print(ans.summary())
    scanned_list = []
    for e in ans:
        #print(e[1].show()) # every packet object has a show method. e has 2 parts
        scanned_list.append((e[1].psrc,e[1].hwsrc)) #(ip,mac)
        #print(f"ip= {e[1].psrc} , mac= {e[1].hwsrc} ")
        #print('-'*60)
    return scanned_list    
#    
def print_result(scanned_list):
    for t in scanned_list:
        print(f"ip= {t[0]} \t\t mac= {t[1]}")
        print('-'*60)
#main        
options = get_arguments()
#scan_result = scan("10.0.2.1/24")
scan_result = scan(options.target)
print_result(scan_result)    
