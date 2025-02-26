import socket
server_name = "127.0.0.1"                                   # TODO change to the IP address of the auth server on current network
server_port = 341

# creating socket and connecting to auth server
auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
auth.connect((server_name, server_port))

# confirming connection
connected = False
request = "Door PI"
auth.send(request.encode())
print("Confirmation request sent")
confirmation = auth.recv(64).decode()
if confirmation is not "Auth Server":
      auth.close()
      print("Connected server is not the auth server\nConnection closed")
else:
      connected = True
      print("Auth server confirmed")


# function to unlock the door
def unlock_door():
      print("Door is unlocked")

while connected:
      # sending RFID scan to server
      rfid = input("Input: ")                               # TODO change to proxmark input
      auth.send(rfid.encode())

      # receiving and printing response from server
      response = auth.recv(64)
      verified = True if response is "RFID verified" else False

      if verified:
            print("RFID card verified. Access confirmed")
            unlock_door()

# closing connection to server
auth.close()
