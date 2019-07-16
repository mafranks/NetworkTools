#!/usr/bin/python3

import socket
import ipaddress
from queue import Queue
import threading
import argparse

parser = argparse.ArgumentParser(description="Look for open ports on a host or range of hosts.")
parser.add_argument('--iprange', help="Provide IP or IP range (CIDR notation).")
parser.add_argument('--sport', help="Lowest port.")
parser.add_argument('--eport', help="Highest port.")
args = parser.parse_args()

count = 0
iplist = []
NUMTHREADS = 250
q = Queue()

if args.iprange:
        iprange = args.iprange
else:
        iprange = input("Enter IP range to check: ").strip()
if args.sport:
        sport = int(args.sport)
else:
        sport = int(input("Enter first port in range you want to check: ").strip())
if args.eport:
        eport = int(args.eport)
else:
        eport = int(input("enter last port in range you want to check: ").strip())

def Connector(ip):
    for i in range(sport, eport):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.6)
            result = sock.connect_ex((str(ip),i))
            sock.close()
            if result == 0:   # 0 indicates a successful connection
                print(f"\033[92mPort {i} Open on {ip}\033[0m")     #\033[92m starts green text and \033[0m resets to default
            
        except Exception as e:
            print(e)

# For each IP, scan the selected port range
def threader():
    while True:
        worker = q.get()
        Connector(worker)
        q.task_done()

# Determine how many IPs are being scanned and add them to a list
for ip in ipaddress.IPv4Network(iprange):
    count += 1
    iplist.append(str(ip))

# Set up threading to make this blazing fast    
for x in range(int(NUMTHREADS)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Set up a worker for each IP
for worker in iplist:
    q.put(worker)
q.join()

print("*"*30)
print(f"\033[92mProcessing Complete!\033[0m")
print("*"*30)
