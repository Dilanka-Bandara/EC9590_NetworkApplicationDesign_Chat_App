import socket
import threading
import json

# Configuration
HOST = '127.0.0.1'
PORT = 55555

# Dictionary to map 'username' -> 'client_socket'
active_clients = {}

def handle_client(client_socket, client_address):
    username = None
    try:
        # Receive username upon connection
        username = client_socket.recv(1024).decode('utf-8')
        
        if username in active_clients:
            client_socket.send("Username already taken.".encode('utf-8'))
            client_socket.close()
            return

        active_clients[username] = client_socket
        print(f"[CONNECTED] New client: {username}")
        
        # Send welcome message
        welcome_msg = {
            "status": "1",
            "sender": "Server",
            "receiver": username,
            "text": "Connected! Type 'exit' to leave."
        }
        client_socket.send(json.dumps(welcome_msg).encode('utf-8'))

        # Main Listener Loop
        while True:
            message_data = client_socket.recv(1024).decode('utf-8')
            
            # If recv returns empty bytes, the client has disconnected
            if not message_data:
                break
            
            try:
                msg_json = json.loads(message_data)
                target_user = msg_json.get('receiver')
                sender = msg_json.get('sender')
                text = msg_json.get('text')

                # Check if the user explicitly sent an "exit" message
                if text.lower() == 'exit':
                    break

                # Forwarding Logic (Task 03)
                if target_user in active_clients:
                    target_socket = active_clients[target_user]
                    target_socket.send(json.dumps(msg_json).encode('utf-8'))
                    print(f"[FORWARD] {sender} -> {target_user}")
                else:
                    # Send error if user not found
                    error_msg = {
                        "status": "0", "sender": "Server", "receiver": sender,
                        "text": f"Error: User '{target_user}' is not online."
                    }
                    client_socket.send(json.dumps(error_msg).encode('utf-8'))

            except json.JSONDecodeError:
                pass

    except ConnectionResetError:
        pass 
    finally:
        # === NEW FUNCTION: BROADCAST EXIT ===
        if username and username in active_clients:
            del active_clients[username]
            print(f"[DISCONNECT] {username} has left.")
            
            # Create the exit notification message
            exit_announcement = {
                "status": "1",
                "sender": "Server", 
                "receiver": "All",
                "text": f"User '{username}' has left the chat."
            }
            
            # Loop through all remaining clients and send the notification
            for user, socket_obj in active_clients.items():
                try:
                    socket_obj.send(json.dumps(exit_announcement).encode('utf-8'))
                except:
                    pass # Ignore errors if sending to a stale socket
                    
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Server listening on {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    start_server()