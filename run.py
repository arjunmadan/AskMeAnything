from flask import Flask, request, redirect
import twilio.twiml
import urllib
import urllib2
import logging
import sys
import xml.etree.ElementTree as ET
import goslate

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

wolfram_api = 'TRR8TK-VHV99K9UE8'

gs = goslate.Goslate()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""
	from_number = request.values.get('From', None)
	content = request.values.get('Body', None)
	message = ""
	title_list = ["Definition", "Pronounciation", "Result", "Basic information", "Leadership position", "Notable facts", "Distance", "Company information", "Properties", "Name"]
	language = "en"
	if is_ascii(content) and len(content.split(' ')) > 1:
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
		logging.warning("entering if")
		for pod in root:
			if pod.tag == "pod":
				for it in title_list:
					if pod.attrib['title'] == it:
						subpod = pod[0]
						message += gs.translate(subpod[0].text, language)
	else:
		if is_ascii(content) == false and len(content.split(' ')) == 1:
			logging.warning("entering second if")
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
				for pod in root:
					if pod.tag == "pod":
						for it in title_list:
							if pod.attrib['title'] == it:
								subpod = pod[0]
								message += gs.translate(subpod[0].text, language)
			
	if message == "": 
		message = gs.translate("Your query turned up no results. Please try something else.", language)
	logging.warning(message)
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
		
if __name__ == "__main__":
	app.run(debug=True)
