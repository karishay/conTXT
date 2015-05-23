from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('./config.py')

dict_of_responses = []

@app.route('/recieve_data', methods=["GET","POST"])
def recieve_data():
    """Recieves incoming text data"""
    sms_body = request.values.get("Body")
    dict_of_responses.append(sms_body)
    resp = twilio.twiml.Response()
    resp.message()
    print dict_of_responses
    return str(resp)


if __name__ == '__main__':
    app.run(port=5051)
