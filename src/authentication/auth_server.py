import socket

# Socket IP and port
server_host = "192.168.1.175"                       # TODO Change IP address to auth server
server_port = 25341

# Setting up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', server_port))
server.listen(1)
print(f"Server listening on port {server_port}")
print ("Socket created\n")

# Function to authenticate the rfid signals
def authenticate(rfid):													# TODO Create authentication process
	valid_rfids = ["3400735b41"]
	return True if rfid in valid_rfids else False

# Server loop
while True:
	try:
		# Waiting for client connection
		print("Waiting for client ...")
		door_pi, addr = server.accept()
		print("Client connected from: ", addr)

		# Confirming client is a door pi
		confirmation = "Auth Server"
		request = door_pi.recv(64).decode()
		print("Confirmation request received: " + request + ".")

		# Closing connection if connected device is not door pi 
		if request != "Door PI":
			door_pi.close()
			print("Request is not coming from a door pi\nConnection closed\n")
		# Continuing with authentication if door pi is confirmed
		else:
			door_pi.send(confirmation.encode())
			print("Request confirmed")

			# Receiving rfid
			rfid = door_pi.recv(64).decode()
			print("RFID received: ", rfid)

			# Authenticating rfid
			verified = authenticate(rfid)
			response = "RFID verified" if verified else "RFID not valid"

			# Sending output back to client
			door_pi.send(response.encode())
			print("Response sent\n")
	except Exception as e:
		print(f"Authentication error: {e}") 
	finally:
		# Closing connection to client
		door_pi.close()
