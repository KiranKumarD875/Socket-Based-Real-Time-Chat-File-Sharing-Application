# Socket-Based Real-Time Chat & File Sharing Application

A real-time multi-client chat application built using Python TCP sockets that supports live text messaging and file sharing.  
The project follows a client–server architecture and uses multithreading to handle multiple users concurrently.

---

## 📌 Features

- Real-time text chat between multiple clients
- File sharing support (any file type)
- TCP-based reliable communication
- Multi-client handling using threading
- Nickname-based user identification
- Centralized server architecture
- Runs on localhost or LAN

---

## Technologies Used

- **Programming Language:** Python  
- **Networking:** TCP Sockets  
- **Concurrency:** Multithreading  
- **Environment:** VS Code / Terminal  
- **OS Compatibility:** Windows, Linux, macOS  

---

## Project Structure
Chat-Application-Using-Sockets/
│
├── server.py # Server-side code
├── client.py # Client-side code
├── received_files/ # Folder where received files are stored (optional)
└── README.md

## ⚙️ How It Works

### Client–Server Architecture

- The **server** listens for incoming client connections on a specific IP and port.
- Each **client** connects to the server using a TCP socket.
- A new thread is created on the server for every connected client.
- Messages and files sent by a client are processed and broadcasted to all other clients.

---

## Communication Flow

1. Client connects to server
2. Server requests client nickname
3. Client sends nickname
4. Client chooses:
   - Text message
   - File transfer
5. Server receives data and:
   - Broadcasts text messages
   - Saves received files and notifies other clients

---

## 🚀 How to Run the Project

### Prerequisites

- Python 3.x installed
- VS Code or any terminal-based IDE

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/socket-chat-application.git
cd socket-chat-application
