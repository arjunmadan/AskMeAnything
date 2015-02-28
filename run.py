from flask import Flask, request, redirect
import twilio.twiml
import  wolframalpha
import logging

client = wolframalpha.Client('TRR8TK-VHV99K9UE8')

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
	from_number = request.values.get('From', None)
	content = request.values.get('Body', None)
	
	wolfram_content = client.query(content)
	logging.warning(wolfram_content.results)
	message = next(wolfram_content.results).text

#	print(message)
	
	#if from_number in callers:
	#	message = callers[from_number] + ", thanks for the message!"
	#else:
	#	message = "Monkey, thanks for the message!"
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
if __name__ == "__main__":
	app.run(debug=True)
