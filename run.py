from flask import Flask, request, redirect
import twilio.twiml
import  wolframalpha
import logging
import sys

wolfram_api = 'TRR8TK-VHV99K9UE8'

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
	"+19199855863": "Arjun",
	"+19199855965": "Boots",
	"+19197605565": "Virgil",
	}
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""
	try:
		from_number = request.values.get('From', None)
		content = request.values.get('Body', None)
		
		url = "http://api.wolframalpha.com/v2/query?appid=" + wolfram_api + "&input=" + content + "&format=plaintext"
		r = requests.get(url)
		
		logging.warning(r.text)
		#wolfram_content = client.query(content)
		
		#logging.warning(type(wolfram_content))
		#if wolfram_content.results:
		#	message = next(wolfram_content.results).text
		#else:
		#	message = "No results found!"
		#resp = twilio.twiml.Response()
		#resp.message(message)
		#return str(resp)
		
	except:
		logging.warning("Error")
		message="No results found. Try an alternate question."
		#resp = twilio.twiml.Response()
		#resp.message(message)
		#return str(resp)
	
if __name__ == "__main__":
	app.run(debug=True)
