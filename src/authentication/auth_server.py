import socket
server_host = "127.0.0.1"                                               # TODO change to the IP address of the auth server on current network
server_port = 341

# setting up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', server_port))
server.listen(1)
print ("Socket created\n")

# function to authenticate the rfid signals
def authenticate(rfid):								# TODO create authentication process
	valid_rfids = [0, 1, 2]
	return True if rfid in valid_rfids else False

# server loop
while 1:
	# waiting for client connection
	print("Waiting for client ...")
	door_pi, addr = server.accept()
	print("Client connected from: ", addr)

	# confirming client is a door pi
	confirmation = "Auth Server"
	request = door_pi.recv(64)
	print("Confirmation request received: " + request + ".")

	# closing connection if connected device is not door pi 
	if request != "Door PI":
		door_pi.close()
		print("Request is not coming from a door pi\nConnection closed\n")
	# continuing with authentication if door pi is confirmed
	else:
		door_pi.send(confirmation.encode())
		print("Request confirmed")

		# receiving rfid
		rfid_string = door_pi.recv(64)
		rfid = int(rfid_string)
		print("RFID received: ", rfid)

		# authenticating rfid
		verified = authenticate(rfid)
		response = "RFID verified" if verified else "RFID not valid"

		# sending output back to client
		door_pi.send(response.encode())
		print("Response sent\n")

	# closing connection to client
	door_pi.close()
