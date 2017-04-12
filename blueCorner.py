#******************************************************************#
#
#	Converted the "Build the Void" script to build the blue corner
#	 By Reddit user: azimir
#
#******************************************************************#

import urllib
import urllib2
import time
import json
import random

BLUE = 13

print "Build The Blue Corner script"


print "Getting user agent list for anonymity (please wait)"
user_agent_list=list(set([ua for ua in urllib.urlopen("https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/txt/user-agents.txt").read().splitlines() if not ua.startswith("#")]))

accounts = []
sessions = {}

print "For each account you want to use, enter it in like username:password"
print "When you're done, type 'done'"

user_input = ""
while (user_input != "done"):
	user_input = raw_input("Account-> ")
	if user_input.lower() != "done":
		accounts.append(user_input)

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', random.choice(user_agent_list))]
for account in accounts:
	username = account.split(":")[0]
	password = account.split(":")[1]
	data = urllib.urlencode({'op': 'login-main', 'user': username, 'passwd': password, 'api_type': 'json'})
	resp = opener.open('https://www.reddit.com/api/login/'+urllib.quote(username), data).read()
	sessions[username] = json.loads(resp)["json"]["data"]["cookie"]



print "[x] Running Build The Blue Corner"
wait_time = 305 # defaults to 5 minutes after placing a pixel
patrol_count = 1;

#print " DEBUG: Waiting 5 mins to be polite "
#time.sleep(wait_time)

while True:
	# Fill The Blue Corner
	print "[x] Starting patrol #" + str(patrol_count) + " in defense of The Blue Corner!"
	patrol_count += 1

	for session in sessions.keys():
		cookie = sessions[session]
		found_color = BLUE

		for ytest in range(999, 968, -1):
			for xtest in range(999, 965, -1):
			#for xtest in range(962, 900, -1):
				#print "Looking at (" + str(xtest) + "," + str(ytest) + ")"
				try:
					resp = opener.open("https://www.reddit.com/api/place/pixel.json?x="+str(xtest)+"&y="+str(ytest)).read()
				except Exception, e:
					print " [e] Exception on a pixel inspection: " + str(e)
					break
				try:
					found_color = int(json.loads(resp)["color"])
				except Exception, e:
					print " [e] Exception on a json parse for color: ",
					print resp
					found_color = BLUE
				print "  [x] Color at (" + str(xtest) + "," + str(ytest) + ") currently is: " + str(found_color)
				time.sleep(0.3);
				if( found_color != BLUE ):
					break
			if( found_color != BLUE ):
				break

		print ""
		print " [x] TIME TO SHINE: Color at (" + str(xtest) + "," + str(ytest) + ") currently is: " + str(found_color)

		#** Start assembling URL query for non-blue color at (xtest, ytest) **#
		data = urllib.urlencode({'x': xtest, 'y': ytest, 'color': BLUE})
		newopener = urllib2.build_opener()
		newopener.addheaders = [('User-Agent', random.choice(user_agent_list))]
		newopener.addheaders.append(('Cookie', 'reddit_session='+cookie))
		try:
			modhash = json.loads(newopener.open("https://reddit.com/api/me.json").read())["data"]["modhash"]
		except Exception, e:
			print " [e] Modhash failed to work properly with: " + str(e)
			break

		newopener.addheaders.append(('x-modhash', modhash))

		#print " [x] Assembled query, time to change pixel"
		try:
			# Waits 10 seconds to try to change a pixel. If fail... wait wait_time more seconds!
			next=newopener.open("https://www.reddit.com/api/place/draw.json", data, 10).read()
			print next
			try:
				wait_time = int(json.loads(next)["wait_seconds"]) + 6
				print " [x] Next wait time is now: " + str(wait_time) + " seconds"
			except Exception, e:
				wait_time = 305
				print " [e] Failed to read time? Next wait time is now: " + str(wait_time) + " seconds"
			
			# Check to see if we successfully wrote the pixel as intended
			try:
				finalresp = newopener.open("https://www.reddit.com/api/place/pixel.json?x="+str(xtest)+"&y="+str(ytest)).read()
			except Exception, e:
				print " [e] Pixel check failed with: " + str(e)

			if session in finalresp:
				print " [x] Defended The Blue Corner successfully once again!"
			else:
				print finalresp
		except Exception, e:
			print " [!] Pixel update failed."

	print " [x] Time to rest. Waiting " + str(wait_time) + " seconds."
	time.sleep(wait_time)
