import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client, chat_display):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            
            try:
                msg_json = json.loads(message)
                sender = msg_json.get('sender')
                text = msg_json.get('text')
                
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"<{sender}>: {text}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
            except json.JSONDecodeError:
                pass
        except:
            break

def send_message(event=None):
    user_input = entry_msg.get().strip()
    
    if not user_input:
        return

    if user_input.lower() == 'exit':
        client.close()
        root.quit()
        return

    if ":" in user_input:
        target_user, text_content = user_input.split(":", 1)
        json_packet = {
            "status": "1",
            "sender": username,
            "receiver": target_user.strip(),
            "text": text_content.strip()
        }
        client.send(json.dumps(json_packet).encode('utf-8'))
        
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You (to {target_user.strip()}): {text_content.strip()}\n")
        chat_display.config(state=tk.DISABLED)
        entry_msg.delete(0, tk.END)
    else:
        messagebox.showwarning("Format Error", "Use format 'Recipient: Message'")

# --- GUI and Network Setup ---
root = tk.Tk()
root.withdraw() # Hide main window until logged in

username = simpledialog.askstring("Login", "Input your user name:")
if not username:
    exit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    client.send(username.encode('utf-8'))
except:
    messagebox.showerror("Error", "Could not connect to server.")
    exit()

# Show main window
root.deiconify() 
root.title(f"Task 3 Chat - Logged in as {username}")

chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=50, height=20)
chat_display.pack(padx=10, pady=10)

# Welcome instructions
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "Commands:\n1. To Chat: 'Recipient: Message'\n2. To Exit: Type 'exit'\n------------------------\n")
chat_display.config(state=tk.DISABLED)

entry_msg = tk.Entry(root, width=40)
entry_msg.pack(side=tk.LEFT, padx=(10, 0), pady=10)
entry_msg.bind("<Return>", send_message)

btn_send = tk.Button(root, text="Send", command=send_message)
btn_send.pack(side=tk.LEFT, padx=10, pady=10)

recv_thread = threading.Thread(target=receive_messages, args=(client, chat_display))
recv_thread.daemon = True
recv_thread.start()

if __name__ == "__main__":
    root.mainloop()