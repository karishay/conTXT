from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml
import json


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('./config.py')

#TODO: later, turn this into a database
dict_of_responses = {"True": {"feb 3rd, 2015": [1,2,3,4,5,3,4,3]}, "False":[{"april 18th, 2015": [1,2,3,3,2,1]}]}

@app.route('/recieve_data', methods=["GET","POST"])
def recieve_data():
    """Recieves incoming text data, if "True" is not None, add to list"""
    if dict_of_responses["True"] != None:
        sms_body = request.values.get("Body")
        #get the name of the recording
        recording_name = dict_of_responses["True"].keys()[0]
        #look up by name of recording and add the sms to the list
        dict_of_responses["True"][recording_name].append(sms_body)
    resp = twilio.twiml.Response()
    resp.message()
    print dict_of_responses
    return str(resp)

@app.route('/list_of_recordings')
def list_of_recordings():
    """ Returns all names of recordings and which ones are active"""
    #name of the active recording
    active = dict_of_responses["True"].keys()[0]
    #name of all other recordings
    inactive = []
    for recording_name in dict_of_responses["False"]:
        inactive.append(recording_name.keys()[0])

    all_recordings = {"active": active, "inactive": inactive}
    return json.dumps(all_recordings)

@app.route('/start_recording/<name_of_recording>')
def start_recording(name_of_recording):
    """ Given a name, check to see if there's a recording in the dict
    with that name, if so, set to active, if not, move current active to
    false and set new name to active """
    #if name_of_recording == key in dict_of_responses[1]
        #add
    #return render_template("start_recording.json", recording_name=name_of_recording)
    return "Yay, name of recording is %s" % name_of_recording

@app.route('/stop_recording/<name_of_recording>')
def stop_recording(name_of_recording):
    """ Given a name of a recording, if that name is in "True", move it to
    "False" and set "True" to None, if it is not in "True", return an error """
    return "You wanna stop recording on %s" % name_of_recording


if __name__ == '__main__':
    app.run(port=5051)
