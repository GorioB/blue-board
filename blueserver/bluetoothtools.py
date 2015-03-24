from bluetooth import *
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","blueserver.settings")
from notices.models import Notice,UserProfile
from django.utils.dateformat import format
from django.db.models import Q
import datetime
import json
import django
import signal
import sys
django.setup()

def signal_handler(signal,frame):
	sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
server_sock = BluetoothSocket(RFCOMM)
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "fa87c0d0-afac-11de-8a39-0800200c9a67"

	
advertise_service( server_sock, "SampleServer",
	service_id = uuid,
	service_classes = [uuid, SERIAL_PORT_CLASS ],
	profiles = [SERIAL_PORT_PROFILE],
	)

print "Waiting for connection on RFCOMM channel %d" % port
client_sock,client_info = server_sock.accept()
print "Accepted connection from ",client_info
while True:
	try:
		data = client_sock.recv(1024)
		print data
		try:
			jdata = json.loads(data)
		except:
			jdata = json.loads("{'packet':'PASS'}")
		if jdata['packet']=="ANNOUNCEMENTS_GET":
			result = []
			for i in Notice.objects.filter(Q(del_date__gte=datetime.datetime.now())):
				result.append({"title":i.title,
					"tags":[tag for tag in i.tags.split(",")],
					"author":i.author,
					"body":i.body,
					"pub_date":format(i.pub_date,'U'),
					"del_date":format(i.del_date,'U')})
			jdump = json.dumps({'packet':"ANNOUNCEMENTS_DATA","data":result})
			print jdump
			client_sock.send(jdump)
		if jdata['packet']=="ANNOUNCEMENTS_ADD":
			matchingPins = UserProfile.objects.filter(userKey=jdata['pin'])
			if not matchingPins:
				pass
			else:
				author = matchingPins[0].name
				notice = Notice.objects.create(
					title=jdata['data']['title'],
					tags=",".join(jdata['data']['tags']),
					author=author,
					body = jdata['data']['body'],
					pub_date = datetime.datetime.now(),
					del_date = datetime.datetime.now()+datetime.timedelta(hours=int(jdata['data']['expiry']))
					)
				notice.save()
		if jdata['packet']=="PASS":
			pass
		if jdata['packet']=="QUIT":
			break

		print ("Completed communication, accepting next host")
		client_sock.close()
		client_sock,client_info=server_sock.accept()
		print ("Accepted connection from ",client_info)

	except IOError:
		client_sock.close()
		client_sock,client_info = server_sock.accept()
		print ("Accepted connection from ",client_info)

print "disconnected"
client_sock.close()
server_sock.close()
print "All done"