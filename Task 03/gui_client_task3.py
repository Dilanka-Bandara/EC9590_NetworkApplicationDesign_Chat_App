import socket
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 55555

# --- STYLING CONSTANTS ---
BG_COLOR = "#2C3E50"
FG_COLOR = "#ECF0F1"
BTN_COLOR = "#2980B9"
FONT = ("Helvetica", 12)

def send_message():
    # 1. Create socket (Your original logic)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to server
    try:
        client.connect((HOST, PORT))
    except:
        messagebox.showerror("Connection Error", "Could not connect.")
        return

    # 3. Send a message
    msg = entry_msg.get()
    client.send(msg.encode('utf-8'))

    # 4. Receive acknowledgement
    response = client.recv(1024).decode('utf-8')
    lbl_response.config(text=f"Server response: {response}")

    # 5. Close
    client.close()

# --- BEAUTIFUL GUI SETUP ---
root = tk.Tk()
root.title("Task 1 - Chat App")
root.geometry("400x200")
root.configure(bg=BG_COLOR)

tk.Label(root, text="Enter message to send to server:", bg=BG_COLOR, fg=FG_COLOR, font=FONT).pack(pady=(20, 5))

entry_msg = tk.Entry(root, width=35, font=FONT, bg="#34495E", fg=FG_COLOR, insertbackground=FG_COLOR, relief=tk.FLAT)
entry_msg.pack(pady=5, ipady=5)

tk.Button(root, text="Send Message", command=send_message, bg=BTN_COLOR, fg="white", font=("Helvetica", 12, "bold"), relief=tk.FLAT, activebackground="#1F618D", activeforeground="white").pack(pady=10)

lbl_response = tk.Label(root, text="Waiting for response...", bg=BG_COLOR, fg="#AAB7B8", font=("Helvetica", 10, "italic"))
lbl_response.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()