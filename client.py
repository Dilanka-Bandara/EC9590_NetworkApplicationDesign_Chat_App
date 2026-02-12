import socket
import threading
import sys
import json

# Configuration
HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client_socket):
    """
    Listens for incoming messages from the server in a separate thread.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\n[Disconnected from server]")
                client_socket.close()
                sys.exit()
            
            try:
                # Parse JSON message
                msg_json = json.loads(message)
                sender = msg_json.get('sender')
                text = msg_json.get('text')
                
                # We use \r to clear the current line so the incoming message 
                # doesn't mess up your typing bar.
                print(f"\r<{sender}>: {text}\nYou: ", end="", flush=True)
            except json.JSONDecodeError:
                print(f"\r{message}\nYou: ", end="", flush=True)
                
        except Exception as e:
            print(f"\n[Error] Connection lost: {e}")
            client_socket.close()
            sys.exit()
            break

def start_client():
    # Task 01: Create socket and connect
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running?")
        return

    # User Login
    username = input("Input your user name: ")
    client.send(username.encode('utf-8'))

    print(f"Logged in as {username}. Usage: 'TargetUser: Message'")
    print("------------------------------------------------------")

    # Task 02: Handle concurrency (receiving while sending)
    # On Windows, we use a Thread instead of select() for the 'listening' part.
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True # Thread dies when main program dies
    recv_thread.start()

    # Main Loop: Handle User Input (Sending)
    while True:
        try:
            user_input = input("You: ") # Simple blocking input
            
            if not user_input:
                continue

            # Parse input to extract Target and Message
            if ":" in user_input:
                target_user, text_content = user_input.split(":", 1)
                target_user = target_user.strip()
                text_content = text_content.strip()

                # Task 03: JSON structure
                json_packet = {
                    "status": "1",
                    "sender": username,
                    "receiver": target_user,
                    "text": text_content
                }
                client.send(json.dumps(json_packet).encode('utf-8'))
            else:
                print("[System]: Invalid format. Use 'Recipient: Message'")

        except KeyboardInterrupt:
            print("\nExiting...")
            client.close()
            sys.exit()

if __name__ == "__main__":
    start_client()