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
    active = dict_of_responses["True"].keys()[0]
    print "I am the active: %s" % active
    print "I am the name passed in the url: %s" % name_of_recording
    inactive = []
    for recording_name in dict_of_responses["False"]:
        inactive.append(recording_name.keys()[0])

    if active == name_of_recording:
        return "You're recording : %r" % name_of_recording
    elif name_of_recording in inactive:
        #save current name_of_recording (and data) within inactive to a variable
        #iterate through the list of "False" recordings
        for n in dict_of_responses["False"]:
            print "woah n: %s" % dict_of_responses["False"].index(n)
            # if that item is the same as the one we are looking for
            if n.keys()[0] == name_of_recording:
                # save it in a temp variable
                print "The name given was in the false dict, which right now looks like: %r" % dict_of_responses["True"]
                new_active = {name_of_recording:n[name_of_recording]}
                # reset the value to whatever is in the active spot
                old_active = dict_of_responses["True"]
                if old_active.keys()[0] not in dict_of_responses["False"]:
                    print " old is not in inactive, so add it: %s" % old_active.keys()[0]
                    #delete the one that is getting promoted to active from false
                    indice = dict_of_responses["False"].index(n)
                    dict_of_responses["False"][indice]= old_active
                print "Tried to add %s to the false dict:" % old_active
                print "Did it work? : %s" % dict_of_responses["False"]
                # reset the active spot to the one with the name we are looking for
                dict_of_responses["True"] = new_active
                return "I have changed the active to %r " % new_active
    else:
        #if active not None
        if active != None:
            print "before adding to false dict: %r" % dict_of_responses["False"]
            dict_of_responses["False"].append(dict_of_responses["True"])
            print "this is what I've added to the false dicts: %r" % dict_of_responses["True"]
            print "This is what it looks like now: %r" % dict_of_responses["False"]
            # add active to inactive (False)
        dict_of_responses["True"] = {name_of_recording: []}
    #return render_template("start_recording.json", recording_name=name_of_recording)
        return "Yay, name of recording is %s" % name_of_recording

@app.route('/stop_recording/<name_of_recording>')
def stop_recording(name_of_recording):
    """ Given a name of a recording, if that name is in "True", move it to
    "False" and set "True" to None, if it is not in "True", return an error """
    return "You wanna stop recording on %s" % name_of_recording


if __name__ == '__main__':
    app.run(port=5051)
