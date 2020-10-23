# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:11:48 2019

@author: ljmg1
"""


import http.client
import json
import time

import csv

codes = []
conn = http.client.HTTPSConnection("dev.virtualearth.net")
with open('01.csv', 'r',newline="") as csvfile:
    Myreader = csv.reader(csvfile)
    for item in Myreader:
        long = str(item[17])
        la = str(item[18])
                          
        conn.request("GET","/REST/v1/Locations/"+long+","+la+"?&key=AkahH5mC6nBDfWuTTNdUs2kchB-h5_C-8Yy0Yw9kNxjhPCoICkx0J-IbXhOWFi51")
        r1 = conn.getresponse()
        response = r1.read()
        response_dict = json.loads(response)
        if "postalCode" in response_dict["resourceSets"][0]["resources"][0]["address"].keys():
            code = response_dict["resourceSets"][0]["resources"][0]["address"]["postalCode"]
            codes.append(code)
            time.sleep(0.1)
        else:
            codes.append("0")

with open("02.csv",'w',newline='') as csvfile:
    Mywriter = csv.writer(csvfile)
    for i in range(len(codes)):
        Mywriter.writerow([codes[i]])
"""
"""
import csv
d = {}
with open('01.csv', 'r',newline="") as csvfile:
    Myreader = csv.reader(csvfile)
    for item in Myreader:
        if item[0] not in d.keys():
            d[item[0]] = 1
        else:
            d[item[0]] += 1 
        
with open("02.csv",'w',newline='') as csvfile:
    Mywriter = csv.writer(csvfile)
    for key in d.keys():
        Mywriter.writerow([key,d[key]])
