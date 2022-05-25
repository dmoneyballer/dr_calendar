from email.mime import base
import requests
import json
base_url = 'http://127.0.0.1:5000/'
get_doctors = requests.get(base_url + 'get_doctors')
print('testing get doctors',get_doctors.text)
print('testing get dr appointments')
appointments = requests.get(base_url + 'doctor/1891259164')
print(appointments.text)
print('testing delete appointment')
apt = {'npi': '1891259164', 'apt_id': '18912591641'}
headers = {'content-type': 'application/json'}
deleted = requests.delete(base_url + 'delete_appointment',data=json.dumps(apt), headers=headers)
print(deleted, deleted.text)
deleted = requests.delete(base_url + 'delete_appointment',data=json.dumps(apt), headers=headers)
print(deleted, deleted.text)
print('testing add appointment')
data = {'npi': '1891259164', 'name': 'Travis Pastrana', 'time': '9:00'}
added = requests.post(base_url + 'add_appointment', data=json.dumps(data), headers=headers)
print(added,added.text)