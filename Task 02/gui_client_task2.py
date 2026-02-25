import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 55555

def receive_messages(client, chat_display):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"{msg}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
            else:
                break
        except:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, "Disconnected from server.\n")
            chat_display.config(state=tk.DISABLED)
            break

def send_message(event=None):
    msg = entry_msg.get().strip()
    if msg.lower() == 'exit':
        client.close()
        root.quit()
        return
    
    if msg:
        client.send(msg.encode('utf-8'))
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {msg}\n")
        chat_display.config(state=tk.DISABLED)
        entry_msg.delete(0, tk.END)

# --- Network Setup ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Error", "Could not connect to server.")
    exit()

# --- GUI Setup ---
root = tk.Tk()
root.title("Task 2 Chat")

chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=40, height=15)
chat_display.pack(padx=10, pady=10)

entry_msg = tk.Entry(root, width=30)
entry_msg.pack(side=tk.LEFT, padx=(10, 0), pady=10)
entry_msg.bind("<Return>", send_message) # Allows pressing Enter to send

btn_send = tk.Button(root, text="Send", command=send_message)
btn_send.pack(side=tk.LEFT, padx=10, pady=10)

# Start receive thread
recv_thread = threading.Thread(target=receive_messages, args=(client, chat_display))
recv_thread.daemon = True
recv_thread.start()

if __name__ == "__main__":
    root.mainloop()