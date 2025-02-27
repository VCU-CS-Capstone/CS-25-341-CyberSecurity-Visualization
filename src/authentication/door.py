import socket
server_name = "127.0.0.1"                                               # TODO change to the IP address of the auth server on current network
server_port = 341
rfid = 0

# creating socket
auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# function to unlock the door
def unlock_door():
      print("Door is unlocked\n")
      rfid = 0

# function to send rfid to server for authentication
def authenticate(rfid):
      # connecting to auth server
      auth.connect((server_name, server_port))
      print("Connecting to auth server ...")

      # confirming connection
      request = "Door PI"
      auth.send(request.encode())
      print("Confirmation request sent")
      confirmation = auth.recv(64).decode()

      # closing connection if auth server is not reached
      if confirmation is not "Auth Server":
            auth.close()
            print("Connected server is not the auth server\nConnection closed\n")
      # continuing with authentication if auth server is confirmed
      else:
            print("Auth server confirmed")

            # receiving and printing response from server
            auth.send(rfid.encode())
            print("RFID sent")
            response = auth.recv(64)
            verified = True if response is "RFID verified" else False

            if verified:
                  print("RFID card verified. Access confirmed")
                  unlock_door()

      # closing connection to server
      auth.close()

# authentifaction loop
while 1:
      # waiting for RFID scan
      print("Waiting for RFID scan ...")
      while not rfid:
            rfid = input("Input: ")                                                 # TODO change to proxmark input
      
      # sending to server for authentication
      authenticate(rfid)
