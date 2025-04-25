import socket
import time
from collections import defaultdict

# TODO Lines
#   9
#   20

# Socket IP and port
server_host = "192.168.1.174"                       # TODO Change IP address to auth server
server_port = 25341

# Setting up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', server_port))
server.listen(1)
print(f"Server listening on port {server_port}")
print ("Socket created\n")

# Rate limiting parameters
MAX_CONNECTIONS = 50
TIME_WINDOW = 10
BLOCK_DURATION = 20
connection_log = defaultdict(list)
blocked_ips = {}

# Function to authenticate the rfid signals
def authenticate(rfid):													# TODO Create authentication process
	valid_rfids = ["3400735b41"]
	return True if rfid in valid_rfids else False

# Server loop
while True:
	try:
		# Removing expired blocks
		current_time = time.time()
		expired_blocks = [ip for ip, unblock_time in blocked_ips.items() if current_time >= unblock_time]
		for ip in expired_blocks:
			print(f"Unblocking IP {ip}")
			del blocked_ips[ip]

		# Waiting for client connection
		print("Waiting for client ...")
		door_pi, addr = server.accept()
		ip = addr[0]

		# Checking if IP is blocked
		if ip in blocked_ips:
			print(f"Blocked IP {ip} tried to connect.")
			door_pi.close()
			continue

		# Updating connection log
		connection_log[ip] = [t for t in connection_log[ip] if current_time - t < TIME_WINDOW]
		connection_log[ip].append(current_time)

		# Blocking if too many connections
		if len(connection_log[ip]) > MAX_CONNECTIONS:
			print(f"Too many connections from {ip}. Blocking for {BLOCK_DURATION} seconds.")
			blocked_ips[ip] = current_time + BLOCK_DURATION
			door_pi.close()
			continue

		# Confirming client is a door pi
		print("Client connected from: ", addr)
		confirmation = "Auth Server"
		request = door_pi.recv(64).decode()
		print("Confirmation request received: " + request + ".")

		# Closing connection if connected device is not door pi 
		if request != "Door PI":
			door_pi.close()
			print("Request is not coming from a door pi\nConnection closed\n")
			continue

		# Continuing with authentication if door pi is confirmed
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
