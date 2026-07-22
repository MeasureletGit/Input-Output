import os
import json
import datetime
from pip._vendor import requests  # https://stackoverflow.com/questions/48775755/importing-requests-into-python-using-visual-studio-code
import time

# Determine directories
lib = os.path.dirname(os.path.realpath(__file__)) + os.sep
temp_dir = os.path.join(lib.split('lib')[0], 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# File to store pending measurements
pending_file = os.path.join(temp_dir, 'pending_measurements.json')

# Ensure pending file exists
if not os.path.exists(pending_file):
    with open(pending_file, 'w') as f:
        json.dump([], f)

fluidmonitor_url = 'https://dev.fluidbalancemonitor.com/api/public/device/events'

def uploadmeasurement(mass, iottype, comment=''):
    bedpan_weight = 0
    with open('configuration.txt', 'r') as r:
        con = r.readline().strip()
        cprn = con.split(';')[1]

    measurementtime = time.time()
    createdTime = str(datetime.datetime.fromtimestamp(int(measurementtime)).isoformat())

    with open('setup.txt', 'r') as stp:
        scale_type = stp.readline().strip()
        
    if scale_type == 'output':
        msg = {
            "messageType": "measurement",
            "payload": [{
                "measurementId": "0",
                "cprNumber": cprn,
                "patientName": "",
                "customerId": "",
                "createdTime": createdTime,
                "weight": int(mass),
                "type": iottype,
                "comment": comment,
                "deviceId": "Alex_test_1",
                "bedpanWeight": bedpan_weight
            }]
        }
    elif scale_type == 'input':
        msg = {
            "messageType": "measurement",
            "payload": [{
                "measurementId": "0",
                "cprNumber": cprn,
                "patientName": "",
                "customerId": "",
                "createdTime": createdTime,
                "weight": mass,
                "type": iottype,
                "comment": comment,
                "deviceId": "Alex_test_1",
                "bedpanWeight": 0
            }]
        }
    else:
        print("Unknown scale type")
        return

    headers = {"Content-type": "application/json"}
    print("Uploading measurement:", msg)
    try:
        r = requests.post(fluidmonitor_url, data=json.dumps(msg), headers=headers)
        # Check if the upload was successful
        if r.status_code != 200:
            print("Upload failed with status code", r.status_code)
            save_pending_measurement(msg)
        else:
            print("Upload succeeded")
    except Exception as e:
        print("Error during upload:", e)
        save_pending_measurement(msg)

def sync_measurements():
    """Attempt to upload all pending measurements from the file."""
    try:
        with open(pending_file, 'r') as f:
            pending = json.load(f)
    except Exception:
        pending = []
    
    if not pending:
        print("No pending measurements to sync.")
        return
    
    headers = {"Content-type": "application/json"}
    successful = []
    for msg in pending:
        try:
            print("Syncing pending measurement:", msg)
            r = requests.post(fluidmonitor_url, data=json.dumps(msg), headers=headers)
            if r.status_code == 200:
                successful.append(msg)
                print("Sync succeeded for a measurement.")
            else:
                print("Failed to sync measurement with status", r.status_code)
        except Exception as e:
            print("Exception during sync:", e)
    
    # Remove successfully uploaded messages from pending list
    if successful:
        pending = [msg for msg in pending if msg not in successful]
        with open(pending_file, 'w') as f:
            json.dump(pending, f)
        print(f"Synced {len(successful)} measurements.")
    else:
        print("No measurements were synced successfully.")

def save_pending_measurement(msg):
    """Append a measurement message to the pending file."""
    try:
        with open(pending_file, 'r') as f:
            pending = json.load(f)
    except Exception:
        pending = []
    pending.append(msg)
    with open(pending_file, 'w') as f:
        json.dump(pending, f)



#uploadmeasurement(125, "I", comment='Test med knap1')
#time.sleep(4)
#uploadmeasurement(350, "I", comment='Test med knap2')

if __name__ == "__main__":
    sync_measurements()