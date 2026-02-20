import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                print(f"\n{msg}")
                print("You: ", end="", flush=True)
            else:
                break
        except:
            print("Disconnected from server. Exiting.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start a thread to listen for messages continuously
    # This allows us to Type (main thread) and Receive (recv_thread) simultaneously
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    print("Connected! Type 'exit' to quit.")
    print("You: ", end="", flush=True)

    while True:
        msg = sys.stdin.readline().strip()
        if msg.lower() == 'exit':
            break
        client.send(msg.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    start_client()