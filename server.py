# server.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

clients = {}
client_sockets = []

def handle_client(client_socket, address):
    try:
        hostname = client_socket.recv(1024).decode()
        clients[client_socket] = (hostname, address[0])
        update_client_list()

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
    except:
        pass
    finally:
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]
            update_client_list()

def accept_clients():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[+] Server läuft auf {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Verbindung von {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def update_client_list():
    client_listbox.delete(0, tk.END)
    for idx, (client, (hostname, ip)) in enumerate(clients.items()):
        client_listbox.insert(idx, f"{hostname} - {ip}")

def send_command():
    selection = client_listbox.curselection()
    if not selection:
        messagebox.showwarning("Warnung", "Kein Client ausgewählt!")
        return
    command = command_entry.get()
    if not command:
        messagebox.showwarning("Warnung", "Kein Befehl eingegeben!")
        return
    selected_client = list(clients.keys())[selection[0]]
    try:
        selected_client.send(command.encode())
        output_text.insert(tk.END, f"Gesendet: {command}\n")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

def send_preset(cmd):
    command_entry.delete(0, tk.END)
    command_entry.insert(0, cmd)
    send_command()

# GUI Setup
root = tk.Tk()
root.title("Pico Network Control Center")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

client_listbox = tk.Listbox(frame_left, width=40, height=20)
client_listbox.pack()

command_entry = tk.Entry(frame_right, width=40)
command_entry.pack(pady=5)

send_button = tk.Button(frame_right, text="Senden", command=send_command)
send_button.pack(pady=5)

preset_frame = tk.Frame(frame_right)
preset_frame.pack(pady=10)

tk.Button(preset_frame, text="Shutdown", command=lambda: send_preset('shutdown /s /t 1')).grid(row=0, column=0, padx=5, pady=5)
tk.Button(preset_frame, text="Explorer öffnen", command=lambda: send_preset('start explorer')).grid(row=0, column=1, padx=5, pady=5)
tk.Button(preset_frame, text="Nachricht", command=lambda: send_preset('msg * "Hi from Server"')).grid(row=1, column=0, padx=5, pady=5)
tk.Button(preset_frame, text="Restart", command=lambda: send_preset('shutdown /r /t 1')).grid(row=1, column=1, padx=5, pady=5)
tk.Button(preset_frame, text="Exit Client", command=lambda: send_preset('exit')).grid(row=2, column=0, columnspan=2, pady=5)

output_text = scrolledtext.ScrolledText(frame_right, width=40, height=10)
output_text.pack()

threading.Thread(target=accept_clients, daemon=True).start()

root.mainloop()
