from flask import Flask
from flask import request

app = Flask(__name__)
# appointment id is npi + counter started at 1 so each appointment they get should be npi concat (counter, next one would be npi concate+(counter+1)
doctors = {
    '1891259164': 
    {'name': 'Michael Atkerson Worthington', 
    'appointments': 
        {'18912591641': {'name':'Michael Phelps','time': '8:00'},
        }
    }, 
    '1053938811': 
    {'name': 'Joseph Llavina',
     'appointments': {}
    },   
}

@app.route("/")
def hello():
    return "Hello World!"
# get list of all drs
@app.route("/get_doctors")
def get_doctors():
    drs = {}
    for dr in doctors:
        drs[dr] = doctors[dr]['name']
    return drs

# get list off all appointments for a particular doctor accessed by npi
@app.route('/doctor/<npi>')
def get_doctors_appointments(npi):
    return doctors[npi]['appointments']

# delete existing appt
@app.route('/delete_appointment', methods=['DELETE'])
def delete_appointment():
    content_type = request.headers.get('Content-Type')
    x=''
    if (content_type == 'application/json'):
        json = request.json
        # todo use try catch to catch when appt_id doesn't exist... 
        try:
            del(doctors[json['npi']]['appointments'][json['apt_id']])
            return '{} has been removed'.format(json['apt_id'])
        except:
            return 'apt_id didn\'t exist not deleted'
        

# add appointment if in 15 min interval ie 0,15,30,45 doctors can have 3 appointments per timeslot
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        print(request.data, request.json)
        data = request.json
        # grab apts
        if data['time'][-2:] not in ['00', '15', '30', '45']:
            return 'time must end in 00, 15, 30, or 45'
        apts = doctors[data['npi']]['appointments']
        print(apts)
        # check time to make sure there aren't 3 apts in a single time slot
        times = {}
        for apt in apts:
            time = apts[apt]['time']
            if times.get(time, ''):
                times[time] +=1
            times[time] = 1
        if times.get(data['time'], 0) < 3:
            apt_id = data['npi'] + (str(len(apts) +1))
            # add the appointment
            # to_append = {data['npi']: 
            #     {'name': doctors[data['npi']]['name'],
            #     'appointments': doctors[data['npi']]['appointments']  + {apt_id  : {'name': data['name'], 'time': data['time']}}
            #     }
            # }
            # print(to_append)
            new_dict = {**doctors, **{str(apt_id): {'name': data['name'], 'time': data['time']}}}
            print(new_dict)
            doctors[data['npi']]['appointments'].update({str(apt_id): {'name': data['name'], 'time': data['time']}})
            # doctors[data['npi']['appointments'][int(apt_id)]] = {'name': data['name'], 'time': data['time']}
        

    print(doctors)
    return 'yes my dude added with appointment_id of {}'.format(apt_id)



if __name__ == "__main__":
    app.run()
