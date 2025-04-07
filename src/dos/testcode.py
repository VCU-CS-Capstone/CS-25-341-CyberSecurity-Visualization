import subprocess
import time

def jam(rfid):
    #proxmark_dir = "/home/kali/proxmark3"  <- for proxmark testing
    #pm3_path = f"{proxmark_dir}/pm3"  
    #device_port = "/dev/ttyACM0"
    
    print(f"Sending RFID signal for {rfid}...")
    
    try:
        command = f"flipperzero send lf 125khz EM410x {rfid}"
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print("RFID signal sent successfully!")
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error sending RFID signal: {e}")
        print(e.stderr)

def main():
    test_rfid = "128456"
    jam(test_rfid)




# try:
#        command = f"{pm3_path} -p {device_port} -c \"lf em 410x sim {rfid}\"" #<- change 410x depending on what we use?
#        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
#        print("RFID signal sent successfully!")
#        print(process.stdout)
#    except subprocess.CalledProcessError as e:
#        print(f"Error sending RFID signal: {e}")
#        print(e.stderr)

#       time.sleep(2) < put at end of main for testing