
import os
import json
import datetime
from pip._vendor import requests #https://stackoverflow.com/questions/48775755/importing-requests-into-python-using-visual-studio-code
import time

lib = os.path.dirname(os.path.realpath(__file__) ) +os.sep

tempp= lib.split('lib')[0 ] +os.sep +'temp' +os.sep

fluidmonitor_url = 'https://dev.fluidbalancemonitor.com/api/public/device/events'

def uploadmeasurement(mass, iottype, comment=''):
    bedpan_weight = 45
    with open('configuration.txt', 'r') as r:
        con = r.readline().strip()
        cprn = con.split(';')[1]

    measurementtime = time.time()

    createdTime = str(datetime.datetime.fromtimestamp(int(measurementtime)).isoformat())

    with open('setup.txt', 'r') as stp:
        scale_type = stp.readline().strip()
        
    if scale_type == 'output':
        msg = {"messageType": "measurement", "payload": [
            {"measurementId": "0", "cprNumber": cprn, "patientName": "", "customerId": "",
            "createdTime": createdTime, "weight": int(mass)-bedpan_weight, "type": iottype, "comment": comment,
            "deviceId": "rpi_scale_test",
            "bedpanWeight": 45}]}
        headers = {"Content-type": "application/json"}
        print(msg)
        r = requests.post(fluidmonitor_url, data=json.dumps(msg), headers=headers)
    elif scale_type == 'input':
        msg = {"messageType": "measurement", "payload": [
            {"measurementId": "0", "cprNumber": cprn, "patientName": "", "customerId": "",
            "createdTime": createdTime, "weight": mass, "type": iottype, "comment": comment,
            "deviceId": "rpi_scale_test",
            "bedpanWeight": 0}]}
        headers = {"Content-type": "application/json"}
        print(msg)
        r = requests.post(fluidmonitor_url, data=json.dumps(msg), headers=headers)


