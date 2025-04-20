# Zeek Traffic Logging – Baseline vs. Attack Sessions

This project documents the use of [Zeek](https://zeek.org/) to monitor and log network traffic from specific devices (Door1 and Door2) in a local environment for baseline and attack pattern detection.

## Setup Overview

- **Zeek version**: 7.1.1
- **Environment**: macOS
- **Interface Used**: `en0` (Wi-Fi)
- **Target Devices**:
  - Door1 IP: `192.168.1.152`
  - Door2 IP: `192.168.1.157`
- **Monitored Server**: Auth server hosted locally on the same Mac

---

## Commands Used

### Filtering by IP using BPF (Berkeley Packet Filter)
Zeek was run to only capture traffic involving the two devices of interest:
```bash
sudo zeek -i en0 -f "host 192.168.1.152 or host 192.168.1.157"


To organize logs by session, we created timestamped directories and ran Zeek inside them:

mkdir "$(date '+%Y-%m-%d_%H-%M-%S')"
cd "$(date '+%Y-%m-%d_%H-%M-%S')"
sudo zeek -i en0 -f "host 192.168.1.152 or host 192.168.1.157"
