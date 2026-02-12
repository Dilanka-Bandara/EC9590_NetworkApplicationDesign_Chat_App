import socket
import threading
import json

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 55555

# Dictionary to manage clients: {username: client_socket}
# Covers Task 03: Client management [cite: 65]
active_clients = {}

def handle_client(client_socket, client_address):
    """
    Handles a single client connection.
    """
    username = None
    try:
        # Step 1: Receive the username upon connection
        username = client_socket.recv(1024).decode('utf-8')
        
        if username in active_clients:
            client_socket.send("Username already taken. Connection closed.".encode('utf-8'))
            client_socket.close()
            return

        active_clients[username] = client_socket
        print(f"[NEW CONNECTION] User '{username}' connected from {client_address}")
        
        # Notify user they are connected
        welcome_msg = {"status": "1", "sender": "Server", "receiver": username, "text": "Welcome to ClassChat!"}
        client_socket.send(json.dumps(welcome_msg).encode('utf-8'))

        # Step 2: Listen for messages
        while True:
            message_data = client_socket.recv(1024).decode('utf-8')
            if not message_data:
                break
            
            # Parse the JSON message 
            try:
                msg_json = json.loads(message_data)
                target_user = msg_json.get('receiver')
                text_content = msg_json.get('text')
                sender = msg_json.get('sender')

                # Task 03: Forward message to receiving client [cite: 67]
                if target_user in active_clients:
                    target_socket = active_clients[target_user]
                    target_socket.send(json.dumps(msg_json).encode('utf-8'))
                    print(f"[FORWARD] {sender} -> {target_user}")
                else:
                    # Task 03: Handle exception if receiver is not in system 
                    error_msg = {
                        "status": "0", 
                        "sender": "Server", 
                        "receiver": sender, 
                        "text": f"Error: User '{target_user}' is not online."
                    }
                    client_socket.send(json.dumps(error_msg).encode('utf-8'))

            except json.JSONDecodeError:
                print(f"Received malformed JSON from {username}")

    except Exception as e:
        print(f"Error handling client {username}: {e}")
    finally:
        # Cleanup
        if username and username in active_clients:
            del active_clients[username]
            print(f"[DISCONNECT] User '{username}' disconnected.")
        client_socket.close()

def start_server():
    # Task 01: Create, Bind, Listen [cite: 11, 13, 15]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Server is listening on {HOST}:{PORT}")

    while True:
        # Task 01: Accept connection [cite: 16]
        client_sock, addr = server.accept()
        
        # Task 02: Use Thread + Socket for concurrent clients 
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    start_server()