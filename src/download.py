#!/usr/bin/env python3
import requests
# import os
# import re
# import subprocess,smtplib
# import argparse
# import time
def download(url):
    get_response = requests.get(url)
    print(get_response.content)
#    
url = ""    
download(url)

