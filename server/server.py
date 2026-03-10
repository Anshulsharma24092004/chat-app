import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

clients = []
usernames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server started and listening...")

def log_event(message):
    """Write events to server_log.txt"""
    with open("server_log.txt", "a") as log:
        log.write(message + "\n")

def save_chat(message):
    """Save chat messages to chat_history.txt"""
    with open("chat_history.txt", "a") as file:
        file.write(message + "\n")

def broadcast(message):
    """Send message to all connected clients"""
    for client in clients:
        client.send(message.encode())

def handle_client(client):

    while True:
        try:
            message = client.recv(1024).decode()

            if message == "/users":
                user_list = "Online Users: " + ", ".join(usernames)
                client.send(user_list.encode())
                continue

            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"

            print(formatted_message)

            broadcast(formatted_message)
            save_chat(formatted_message)

        except:
            index = clients.index(client)
            username = usernames[index]

            clients.remove(client)
            usernames.remove(username)

            client.close()

            leave_msg = f"{username} left the chat"
            print(leave_msg)

            broadcast(leave_msg)
            log_event(leave_msg)

            break

def receive():

    while True:
        client, address = server.accept()

        print("Connected with", address)

        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        join_msg = f"{username} joined the chat"
        print(join_msg)

        broadcast(join_msg)
        log_event(join_msg)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()