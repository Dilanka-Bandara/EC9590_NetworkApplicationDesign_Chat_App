import socket
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 55555

def send_message():
    # 1. Create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to server
    try:
        client.connect((HOST, PORT))
    except:
        messagebox.showerror("Connection Error", "Could not connect to the server.")
        return

    # 3. Send a message
    msg = entry_msg.get()
    client.send(msg.encode('utf-8'))

    # 4. Receive acknowledgement
    response = client.recv(1024).decode('utf-8')
    lbl_response.config(text=f"Server response: {response}")

    # 5. Close
    client.close()

# --- GUI Setup ---
root = tk.Tk()
root.title("Task 1 Client")
root.geometry("300x150")

tk.Label(root, text="Enter message to send:").pack(pady=5)
entry_msg = tk.Entry(root, width=30)
entry_msg.pack(pady=5)

tk.Button(root, text="Send", command=send_message).pack(pady=5)
lbl_response = tk.Label(root, text="Server response: ")
lbl_response.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()