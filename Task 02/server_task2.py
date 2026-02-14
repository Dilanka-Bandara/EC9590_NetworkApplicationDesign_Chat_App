import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg or msg.lower() == 'exit':
                connected = False
                break
            
            print(f"[{addr}] {msg}")
            # Simple Echo back to prove bidirectional comms works
            client_socket.send(f"Server Echo: {msg}".encode('utf-8'))
            
        except:
            connected = False

    client_socket.close()
    print(f"[DISCONNECT] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # Accept creates a new socket for each client
        client_sock, addr = server.accept()
        # Spin off a new thread for this client
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()