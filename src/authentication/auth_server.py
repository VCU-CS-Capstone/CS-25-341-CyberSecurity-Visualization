import socket
server_port = 341

# setting up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', server_port))
server.listen(1)
print ("Socket created - ready to ")

# waiting for client connection
print("Waiting for client ...")
door_pi, addr = server.accept()
print("Client connected")

# confirming client is a door pi
confirmation = "Auth Server"
request = door_pi.recv(64).decode()
print("Confirmation request received")
if request is not "Door PI":
	door_pi.close()
	print("Request is not coming from a door pi\nConnection closed")
else:
	door_pi.send(confirmation.encode())
	print("Request confirmed")

# function to authenticate the rfid signals
def authenticate(rfid):								# TODO create authentication process
	valid_rfids = [0, 1, 2]
	return True if rfid in valid_rfids else False

while 1:
	# receiving rfid
	rfid = door_pi.recv(64).decode()
	print("RFID received: " + rfid)

	# authenticating rfid
	verified = authenticate(rfid)
	response = "RFID verified" if verified else "RFID not valid"

	# sending output back to client
	door_pi.send(response.encode())
	print("Response sent")

# closing connection to client
door_pi.close()
