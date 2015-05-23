from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('./config.py')

print app.config['ACCOUNT_SID']
print app.config['AUTH_TOKEN']

dict_of_responses = []

@app.route('/recieve_data', methods=["POST"])
def recieve_data():
  """Recieves incoming text data"""
  sms_body = request.values.get("Body")
  dict_of_responses.append(sms_body)
  print dict_of_responses
  return twilio.twiml.Response

if __name__ == '__main__':
    app.run()
