import socket
import subprocess
import threading
import time
import re

# socket ip and port global variables
server_host = "127.0.0.1"                                               # TODO change to the IP address of the auth server on current network
server_port = 341

# global variable to store the latest RFID read
latest_rfid = 0

# function to unlock the door
def unlock_door():
      print("Door is unlocked\n")

# function to send RFID to server for authentication
def authenticate(rfid):
      # creating socket
      auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      try:
            # connecting to auth server
            auth.connect((server_host, server_port))
            print("Connecting to auth server ...")

            # confirming connection
            request = "Door PI"
            auth.send(request.encode())
            confirmation = auth.recv(64).decode()

            # closing connection if auth server is not reached
            if confirmation != "Auth Server":
                  print("Connected server is not the auth server\nConnection closed\n")
            # continuing with authentication if auth server is confirmed
            else:
                  print("Auth server confirmed")

                  # receiving and printing response from server
                  auth.send(str(rfid).encode())
                  response = auth.recv(64).decode()
                  verified = True if response == "RFID verified" else False

                  if verified:
                        print("RFID card verified")
                        unlock_door()
                  else:
                        print("RFID card denied\n")
      # 
      except Exception as e:
        print(f"Authentication error: {e}")
      finally:
            # closing connection to server
            auth.close()

# Function to start and monitor Proxmark3
def run_proxmark3():
      global latest_rfid
    
      try:
            # Start the Proxmark3 process
            process = subprocess.Popen(
                  ["../Proxmark3 Easy/FOR_Proxmark_Easy_512K/PM3_2023_installation_free/client/pm3", "-i"],  # Path to your pm3 executable
                  stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.STDOUT,
                  text=True,
                  bufsize=1
            )
        
            print("Proxmark3 started, setting up card scanning...")
            time.sleep(2)  # give time to initialize
        
            # set up continuous scanning for EM4100 cards
            process.stdin.write("lf em 410x watch\n")
            process.stdin.flush()
        
            # regular expression to match RFID format
            # pattern matches: [#] EM TAG ID: 340078f067 - ( 61543_120_07925863 )
            card_pattern = re.compile(r'\[#\] EM TAG ID: ([0-9a-f]+) -')
        
            # monitor output for card readings
            while True:
                  line = process.stdout.readline().strip()
                  if not line:
                        continue
                
                  print(f"Proxmark3: {line}")
            
                  # check for EM4100 card detection using regex
                  match = card_pattern.search(line)
                  if match:
                        # extract card ID (first group in regex)
                        card_id = match.group(1)
                        print(f"Card detected! ID: {card_id}")
                        latest_rfid = card_id
    
      except Exception as e:
            print(f"Proxmark3 error: {e}")
            if 'process' in locals():
                  process.terminate()

# start proxmark3 monitoring in separate thread
proxmark_thread = threading.Thread(target=run_proxmark3, daemon=True)
proxmark_thread.start()

# authentifaction loop
while True:
      # clear previous RFID value
      rfid = None

      # waiting for RFID scan
      print("Waiting for RFID scan ...")
      while rfid is None:
            if latest_rfid:
                  rfid = latest_rfid
                  latest_rfid = None  # reset so the same card doesn't get processed twice
            time.sleep(0.1)  # delay to prevent CPU hogging

      # sending to server for authentication
      authenticate(rfid)
