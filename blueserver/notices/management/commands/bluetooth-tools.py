from bluetooth import *

class BluetoothServer:
	def __init__(self):
		self.server_sock = BluetoothSocket(RFCOMM)
		self.server_sock.bind(("",PORT_ANY))
		self.server_sock.listen(1)

		self.port = server_sock.getsockname()[1]

		self.uuid = "fa87c0d0-afac-11de-8a39-0800200c9a67"

	def start(self):
		advertise_service( server_sock, "SampleServer",
			service_id = uuid,
			service_classes = [uid, SERIAL_PORT_CLASS ],
			profiles = [SERIAL_PORT_PROFILE],
			)

		print "Waiting for connection on RFCOMM channel %D" % port
		client_sock,client_info = self.server_sock.accept()
		print "Accepted connection from ",client_info
		try:
			while True:
				data = client_sock.recv(1024)
				if len(data)==0: break
				print "received [%s]" % data
				client_sock.send(data)
		except IOError:
			pass

		print "disconnected"
		client_sock.close()
		self.server_sock.close()
		print "All done"