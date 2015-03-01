from flask import Flask, request, redirect
import twilio.twiml
import urllib
import urllib2
import logging
import sys
import xml.etree.ElementTree as ET
import goslate

wolfram_api = 'TRR8TK-VHV99K9UE8'

gs = goslate.Goslate()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""
	from_number = request.values.get('From', None)
	content = request.values.get('Body', None)
	language = gs.detect(content)
	content = gs.translate(content, 'en')
	content = urllib.pathname2url(content)
	url = "http://api.wolframalpha.com/v2/query?appid=" + wolfram_api + "&input=" + content + "&format=plaintext"
		
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req).read()
	f = open("temp.xml", "w")
	f.write(resp)
	f.close()
	tree = ET.parse("temp.xml")
	root = tree.getroot()
	if root.attrib['success'] == "true":
		pod = root[1]
		#if pod.attrib['title'] == logo:
		#	pod = root[2]
		subpod = pod[0]
		message = gs.translate(subpod[0].text, language)
	else:
		message = "No results found!"
	logging.warning(message)
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
		
if __name__ == "__main__":
	app.run(debug=True)
