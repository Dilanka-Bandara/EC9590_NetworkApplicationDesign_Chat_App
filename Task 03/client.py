import socket
import threading
import sys
import json

HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\n[Disconnected from server]")
                client_socket.close()
                sys.exit()
            
            try:
                msg_json = json.loads(message)
                sender = msg_json.get('sender')
                text = msg_json.get('text')
                
                # Print message cleanly over input prompt
                sys.stdout.write(f"\r<{sender}>: {text}\n")
                sys.stdout.write("You: ")
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                pass
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Could not connect to server.")
        return

    username = input("Input your user name: ")
    client.send(username.encode('utf-8'))

    print(f"Logged in as {username}.")
    print("------------------------------------------------------")
    print("Commands:")
    print("1. To Chat:  'Recipient: Message'")
    print("2. To Exit:  Type 'exit'")
    print("------------------------------------------------------")

    # Start listening thread
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            sys.stdout.write("You: ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()

            if not user_input:
                continue

            # === NEW FUNCTION: EXIT COMMAND ===
            if user_input.lower() == 'exit':
                print("Exiting chat...")
                client.close()
                sys.exit() # Completely stops the program
            
            # Normal Message Logic
            if ":" in user_input:
                target_user, text_content = user_input.split(":", 1)
                
                json_packet = {
                    "status": "1",
                    "sender": username,
                    "receiver": target_user.strip(),
                    "text": text_content.strip()
                }
                client.send(json.dumps(json_packet).encode('utf-8'))
            else:
                print("[SYSTEM]: Use format 'Recipient: Message'")

        except KeyboardInterrupt:
            client.close()
            sys.exit()

if __name__ == "__main__":
    start_client()