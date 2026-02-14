import socket

HOST = '127.0.0.1'
PORT = 55555

def start_client():
    # 1. Create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to server
    try:
        client.connect((HOST, PORT))
    except:
        print("Could not connect.")
        return

    # 3. Send a message
    msg = input("Enter message to send: ")
    client.send(msg.encode('utf-8'))

    # 4. Receive acknowledgement
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    # 5. Close
    client.close()

if __name__ == "__main__":
    start_client()