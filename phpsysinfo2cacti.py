import sys
import os
import json
from pprint import pprint

from optparse import OptionParser

modes = ['retrieveJSONFromFile','retrievePlaintextByHTTP','retrieveJSONByHTTP']

parser = OptionParser()

parser.add_option(
					"-m",
					"--mode",
					action='store',
					type='choice',
					dest='mode',
					choices=modes,
					help="retrieve measurement data using a specific retrieval method"
				)

parser.add_option(
					"-u",
					"--url",
					dest="url",
					type="string",
					help="URL to retrieve when using options retrievePlaintextByHTTP or retrieveJSONByHTTP"
				)

parser.add_option(
					"-j",
					"--json",
					dest="file",
					type="string",
					help="File"
				)

parser.add_option(
					"-d",
					"--debug",
					dest="debug",
					default=False,
                  help="print status messages to stdout"
				)

(options, args) = parser.parse_args()

if not options.mode:
	parser.error('--mode missing. Chose from ' + str(modes))

if options.mode != 'retrieveJSONFromFile' and not options.url:
	parser.error('--url missing. Please provide the URL to your phpsysinfo script; e.g. http://domain.tld/phpsysinfo/xml.php?json')

if options.mode == 'retrieveJSONFromFile' and not options.file:
	parser.error('--json missing. Please provide the path to a JSON dump of phpsysinfos output')

if options.mode == 'retrieveJSONFromFile' and not os.path.isfile(options.file):
	parser.error('--json parameter is invalid: File "' + options.file + '" not found')
	
mode = str(options.mode)

if options.debug:
	debug = options.debug
else:
	debug = False

def d(msg):
	if debug:
		#print(str(msg) + "\n")
		print(str(msg))

def selectURL(default):
	if options.url:
		url = options.url
		d('Using URL "' + url + '" passed as an argument')
	else:
		url = default
		d('Using default URL "' + url + '"')
	
	return url

def retrieveJSONByHTTP():
	json = retrieveUrlContents(options.url)
	
	return parseAndExtractJSON(json)

def retrieveJSONFromFile():
	file = open(options.file)
	json = file.read()
	file.close()
	
	return parseAndExtractJSON(json)

def parseAndExtractJSON(jsonRaw):
	jsonParsed = json.loads(jsonRaw)
	#pprint(jsonParsed)
	
	memory = jsonParsed['Memory']['@attributes']
	#pprint(memory)
	
	exclude = ['Percent','Total']
	
	ret = ""
	for key,value in memory.items():
		if key in exclude:
			d('Excluding ' + key + ' from Cacti result (' + value + ')')
			continue
		
		ret = ret + key + ':' + value + ' '
	
	loadAverage = jsonParsed['Vitals']['@attributes']['LoadAvg']
	#pprint(loadAverage)
	
	keys = {0:'One', 1:'Five', 2:'Fifteen'}
	
	loadAverages = loadAverage.split(' ')
	#pprint(loadAverages)
	
	counter = -1
	for value in loadAverages:
		counter += 1
		keyOut = keys[counter]
		ret = ret + keyOut + ':' + value + ' '
	
	return ret
	
# Not implemented yet. Idea: Retrieve the cacti strings from a static file, updated by a cron job running on your hosting server
def retrievePlaintextByHTTP():
	return retrieveUrlContents(options.url)

def retrieveUrlContents(url):
	d('Retrieving URL "' + url + '"')
	
	import requests
	r = requests.get(url)
	
	return r.text

d('Calling function "' + mode + '"')
cacti = locals()[mode]()

print(cacti)

d('Done.')