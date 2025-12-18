import socket
import threading
import os

# Server configuration
HOST = '192.168.254.227'  # Update with your server IP
PORT = 12345

nickname = input("Choose your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "NICKNAME":
                client.send(nickname.encode('utf-8'))
            elif message.startswith("FILE|"):
                # File transfer
                _, filename, filesize = message.split('|')
                filesize = int(filesize)

                print(f"Receiving file: {filename} ({filesize} bytes)")
                with open(f"received_{filename}", "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        file_chunk = client.recv(1024)
                        bytes_received += len(file_chunk)
                        f.write(file_chunk)
                print(f"File '{filename}' received successfully.")
            else:
                print("\n" + message)
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

# Send messages or files to the server
def write():
    while True:
        message_type = input("Type 'msg' to send a message or 'file' to send a file: ").strip().lower()

        if message_type == "msg":
            client.send("TEXT".encode('utf-8'))
            message = f"{nickname}: {input('Enter your message: ')}"
            client.send(message.encode('utf-8'))

        elif message_type == "file":
            client.send("FILE".encode('utf-8'))
            recipient = input("Enter the recipient's nickname: ").strip()
            file_path = input("Enter the full path of the file to send: ").strip()

            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                filesize = os.path.getsize(file_path)

                # Send file metadata
                client.send(f"{recipient}|{filename}|{filesize}".encode('utf-8'))

                # Send the file content
                with open(file_path, "rb") as f:
                    while (chunk := f.read(1024)):
                        client.send(chunk)

                print(f"File '{filename}' sent successfully to {recipient}.")
            else:
                print("File not found. Please check the path.")

# Start threads for receiving and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
