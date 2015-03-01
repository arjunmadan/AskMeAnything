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

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	content = request.values.get('Body', None)
	message = ""
	title_list = ["Definition", "Definitions", "Exact result", "Pronunciation", "Result", "Basic information", "Leadership position", "Notable facts", "Distance", "Company information", "Properties", "Name", "Current result", "Basic properties", "Physical characteristics"]
	language = "en"
	logging.warning("splitting")
	count = 0	
	for i in content:
		if i == ' ':
			language = gs.detect(content)
			content = gs.translate(content, 'en')
			logging.warning(content)
			content = urllib.pathname2url(content)
			break
		
	
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
						if (RepresentsInt(subpod[0].text)):
							message += gs.translate(pod.attrib['title'], language) + ": " + subpod[0].text + " "
						else:
							message += gs.translate(pod.attrib['title'], language) + ": " + gs.translate(subpod[0].text, language) + " "
	else:
		logging.warning("entering else")			
		for i in content:		
			if i == ' ':
				count = 1
			if count == 0:
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
									message += gs.translate(pod.attrib['title'], language) + ": " + gs.translate(subpod[0].text, language) + " "
			
	if message == "": 
		message = gs.translate("Your query turned up no results. Please try something else.", language)
	logging.warning(message)
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
		
if __name__ == "__main__":
	app.run(debug=True)
