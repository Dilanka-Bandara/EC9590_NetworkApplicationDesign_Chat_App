import socket
import select
import sys
import json

# Configuration
HOST = '127.0.0.1'
PORT = 55555

def start_client():
    # Task 01: Create socket and connect 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running?")
        return

    # User Login
    username = input("Input your user name: ") # Matches Fig 3 demo [cite: 85]
    client.send(username.encode('utf-8'))

    print(f"Logged in as {username}. Usage: 'TargetUser: Message'")
    print("------------------------------------------------------")

    while True:
        # Task 02: I/O Multiplexing using select() 
        # We monitor 'sys.stdin' (keyboard) and 'client' (network socket)
        sockets_list = [sys.stdin, client]
        
        # select() blocks until one of the sockets is ready for I/O
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for socks in read_sockets:
            # Case A: Message received from Server
            if socks == client:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    print("Disconnected from server.")
                    sys.exit()
                
                try:
                    msg_json = json.loads(message)
                    sender = msg_json.get('sender')
                    text = msg_json.get('text')
                    # Display format: <Sender>: Message
                    print(f"<{sender}>: {text}") 
                except json.JSONDecodeError:
                    print(message)

            # Case B: Input from User (Keyboard)
            else:
                user_input = sys.stdin.readline().strip()
                if not user_input:
                    continue

                # Parse input to extract Target and Message
                # Expected format: "Bob: Hello there"
                if ":" in user_input:
                    target_user, text_content = user_input.split(":", 1)
                    target_user = target_user.strip()
                    text_content = text_content.strip()

                    # Task 03: JSON structure [cite: 105-110]
                    json_packet = {
                        "status": "1",
                        "sender": username,
                        "receiver": target_user,
                        "text": text_content
                    }
                    client.send(json.dumps(json_packet).encode('utf-8'))
                    # Print to own console (optional, for UI clarity)
                    # print(f"You to {target_user}: {text_content}")
                else:
                    print("[System]: Invalid format. Use 'Recipient: Message'")

if __name__ == "__main__":
    start_client()