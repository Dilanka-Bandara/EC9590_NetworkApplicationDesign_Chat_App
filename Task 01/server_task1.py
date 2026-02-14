import socket

HOST = '127.0.0.1'
PORT = 55555

def start_server():
    # 1. Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Bind and Listen
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Server listening on {HOST}:{PORT}")

    # 3. Accept ONE connection (Blocking)
    client_socket, addr = server.accept()
    print(f"[CONNECTED] Connection from {addr}")

    # 4. Receive message
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Received from client: {message}")

    # 5. Send acknowledgement
    client_socket.send("Message received by server.".encode('utf-8'))

    # 6. Close connection
    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()