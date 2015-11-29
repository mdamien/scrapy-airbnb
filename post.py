import json

def load(small=False):
	DATA = []
	for i, line in enumerate(open('data.jl')):
	    try:
	        DATA.append(json.loads(line))
	    except:
	        print('fail at line', i)
	    if small and i > 1000:
	        break
	for i in DATA:
	    enhance(i)
	return DATA

def enhance(i):
	pass

