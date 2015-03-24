from bluetooth import *
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","blueserver.settings")
from notices.models import Notice
from django.utils.dateformat import format
import json

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
try:
	while True:
		data = client_sock.recv(1024)
		if len(data)==0: break
		print "received [%s]" % data
		if data=="request":
			result = {}
			for i in Notice.objects.all():
				print format(i.pub_date,'U')
				result[i.pk]={"title":i.title,
					"tags":i.tags,
					"author":i.author,
					"body":i.body,
					"pub_date":format(i.pub_date,'U'),
					"del_date":format(i.del_date,'U')}
			print result
			jdump = json.dumps(result)
			client_sock.send(jdump)
except IOError:
	pass

print "disconnected"
client_sock.close()
server_sock.close()
print "All done"