import io
import json
import re

def toText(n):
	with open('data%s.json' % n) as data_file:
	    data = json.load(data_file)

	rvws = data["reviews"]
	cmts = []
	for i in xrange(0,len(rvws)):
		cmmt = rvws[i]["comments"]
		cmmt = re.sub('\s+', ' ', cmmt)
		#cmmt = re.sub('[\r\n]+', ' ', cmmt)
		#cmmt = re.sub('[\n]+', ' ', cmmt)
		cmts.append(cmmt)


	with open('cmts%s' % n, 'w') as f:
		for cmmt in cmts:
			f.write('%s\n' % cmmt)

toText(2)