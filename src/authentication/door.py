import socket
import subprocess
import threading
import time
import re
import os
import glob
import pty

# Socket IP and port
server_host = "192.168.1.175"                       # TODO Change IP address to auth server
server_port = 25341

# Global variable to store the latest RFID read
latest_rfid = None

# Function to unlock the door
def unlock_door():
    print("Door is unlocked\n")

# Function to send rfid to server for authentication
def authenticate(rfid):
    # Creating socket
    auth = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connecting to auth server
        auth.connect((server_host, server_port))
        print("Connecting to auth server ...")

        # Confirming connection
        request = "Door PI"
        auth.send(request.encode())
        confirmation = auth.recv(64).decode()

        # Closing connection if auth server is not reached
        if confirmation != "Auth Server":
            print("Connected server is not the auth server\nConnection closed\n")

        # Continuing with authentication if auth server is confirmed
        else:
            print("Auth server confirmed")
            
            # Receiving and printing response from server
            auth.send(str(rfid).encode())
            response = auth.recv(64).decode()
            verified = response == "RFID verified"
            if verified:
                print("RFID card verified")
                unlock_door()
            else:
                print("RFID card denied\n")
    except Exception as e:
        print(f"Authentication error: {e}")
    finally:
        # Closing connection to server
        auth.close()

# Function to start Proxmark3 and monitor its log file
def run_proxmark3():
    global latest_rfid
    
    # Path to the Proxmark3 executable and device
    proxmark_dir = "/home/kali/proxmark3"
    pm3_path = os.path.join(proxmark_dir, "pm3")
    device_port = "/dev/ttyACM0"
    
    print(f"Using Proxmark3 client at: {pm3_path}")
    print(f"Connecting to device at: {device_port}")
    
    # Find the Proxmark3 log directory
    log_dir = "/home/kali/.proxmark3/logs"
    if not os.path.exists(log_dir):
        print(f"Error: Could not find Proxmark3 logs directory at {log_dir}")
        return

    try:
        # Start the Proxmark3 with the watch command
        master, slave = pty.openpty()
        process = subprocess.Popen(
            [pm3_path, "-p", device_port, "-c", "lf em 410x watch"],
            stdin=slave, stdout=slave, stderr=slave, close_fds=True
        )
                
        # Looping until a log file is created
        print("Checking for Proxmark3 log files")
        log_files = None
        while not log_files:
            # Get the most recent log file
            log_files = sorted(glob.glob(os.path.join(log_dir, "log_*.txt")), reverse=True)
            time.sleep(2)  # Give it time to create the log file

        print("Proxmark3 started with EM410x watch mode")
        log_file = log_files[0]
        print(f"Monitoring Proxmark3 log file: {log_file}")
        
        # Regular expression pattern for EM card ID
        card_pattern = re.compile(r'\[#\] EM TAG ID: ([0-9a-f]+) -')
        
        # Start at the end of the file
        with open(log_file, 'r') as f:
            # Go to the end of the file
            f.seek(0, 2)
            
            # Monitor for new lines
            while True:
                line = f.readline()
                if not line:
                    # No new line, sleep briefly and try again
                    time.sleep(0.1)
                    continue
                
                line = line.strip()
                print(f"Log: {line}")
                
                # Check for EM card detection
                match = card_pattern.search(line)
                if match:
                    card_id = match.group(1)
                    print(f"Card detected! ID: {card_id}")
                    latest_rfid = card_id
    
    except Exception as e:
        print(f"Proxmark3 error: {e}")
    finally:
        if 'process' in locals() and process.poll() is None:
            process.terminate()

# Start the Proxmark3 monitoring in a separate thread
proxmark_thread = threading.Thread(target=run_proxmark3, daemon=True)
proxmark_thread.start()

# Authentication loop
while True:
    # Clear the previous RFID value
    rfid = None
    
    # Wait for RFID scan
    print("Waiting for RFID scan...")
    while rfid is None:
        if latest_rfid:
            rfid = latest_rfid
            latest_rfid = None  # Reset so we don't process the same card twice
        time.sleep(0.1)  # Small delay to prevent CPU hogging
    
    # Send to server for authentication
    authenticate(rfid)