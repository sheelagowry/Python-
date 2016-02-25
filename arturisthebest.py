import argparse

parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path', help='Path to Apache2 log files', default="/home/ssumathi/logs")
parser.add_argument('--top-urls', help="Find top URL-s", action='store_true')
parser.add_argument('--geoip', help ="Resolve IP-s to country codes", action='store_true')
parser.add_argument('--verbosity', help="Increase verbosity", action="store_true")
args = parser.parse_args()


import os
import urllib
import gzip
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
users = {}
total = 0
for filename in os.listdir(args.path):
	if not filename.startswith("access.log"):
		#print "Skipping unknown file:", filename
		continue
	if filename.endswith(".gz"):
		fh = gzip.open(os.path.join(args.path, filename))
	else:
		fh = open(os.path.join(args.path, filename))    
	if args.verbosity:
		print "Going to process:", filename
	for line in fh:
		total = total + 1
		try:
			source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
			method, path, protocol = request.split(" ")
			path = urllib.unquote(path)
			if path.startswith("/~"):
				username, remainder = path[2:].split("/",1)
				#print "User found:", username
				try:
					users[username] = users[username] + 1
				except:
					users[username] = 1

			url = "http://enos.itcollege.ee" + path
			try:
				urls[url] = urls[url] + 1
			except:
				urls[url] = 1

			for keyword in keywords:
				if keyword in agent:
					try:
						d[keyword] = d[keyword] + 1
					except KeyError:
						d[keyword] = 1
					break # Stop searching for other keywords
		except ValueError:
			pass # This will do nothing, needed due to syntax
 
print "----------TOP 5 USERS----------"
print "Total lines:", total
userresult = users.items()
userresult.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in userresult[:5]:
	print keyword, "=", hits, "(", hits * 100 / total, "%)"
print "----------TOP 5 PAGES----------"
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
print "-------------------------------"
