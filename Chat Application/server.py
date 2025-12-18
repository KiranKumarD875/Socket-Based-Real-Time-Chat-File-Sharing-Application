import socket
import threading

# Server configuration
HOST = '192.168.254.227'  # Update with your server IP
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast a message to all clients or a specific recipient
def broadcast(message, sender=None, recipient=None):
    if recipient:  # Send to a specific client
        if recipient in nicknames:
            target_client = clients[nicknames.index(recipient)]
            target_client.send(message)
    else:  # Send to all clients except the sender
        for client in clients:
            if client != sender:
                client.send(message)

# Handle individual client connections
def handle_client(client):
    while True:
        try:
            message_type = client.recv(1024).decode('utf-8')

            if message_type == "TEXT":
                message = client.recv(1024).decode('utf-8')
                broadcast(message.encode('utf-8'), sender=client)

            elif message_type == "FILE":
                # Receive recipient, filename, and filesize
                file_metadata = client.recv(1024).decode('utf-8')
                recipient, filename, filesize = file_metadata.split('|')
                filesize = int(filesize)

                # Notify recipient about the incoming file
                if recipient in nicknames:
                    target_client = clients[nicknames.index(recipient)]
                    target_client.send(f"FILE|{filename}|{filesize}".encode('utf-8'))

                    # Receive file data and send it to the recipient
                    bytes_received = 0
                    while bytes_received < filesize:
                        file_chunk = client.recv(1024)
                        bytes_received += len(file_chunk)
                        target_client.send(file_chunk)
                    
                    print(f"File '{filename}' successfully transferred to {recipient}.")
                else:
                    client.send("ERROR: Recipient not found.".encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            # Handle client disconnection
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                broadcast(f"{nickname} has left the chat.".encode('utf-8'))
                clients.remove(client)
                nicknames.remove(nickname)
            client.close()
            break

# Accept incoming connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request nickname from the client
        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
