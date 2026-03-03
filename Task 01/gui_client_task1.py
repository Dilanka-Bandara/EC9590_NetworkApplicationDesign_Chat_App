import socket
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 55555

# --- MINIMALIST STYLE CONSTANTS ---
BG_WHITE = "#FFFFFF"
HEADER_BG = "#222222"
TEXT_DARK = "#333333"
TEXT_LIGHT = "#777777"
BORDER_COLOR = "#CCCCCC"
FONT_HEADER = ("Helvetica", 11, "bold")
FONT_BODY = ("Helvetica", 10)

def send_message():
    # 1. Create socket (Unchanged)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connect to server (Unchanged)
    try:
        client.connect((HOST, PORT))
    except:
        messagebox.showerror("Connection Error", "Could not connect to the server.")
        return

    # 3. Send a message (Unchanged)
    msg = entry_msg.get()
    client.send(msg.encode('utf-8'))

    # 4. Receive acknowledgement (Unchanged)
    response = client.recv(1024).decode('utf-8')
    lbl_response.config(text=f"Server: {response}")

    # 5. Close (Unchanged)
    client.close()

# --- GUI SETUP ---
root = tk.Tk()
root.title("Task 1 Client")
root.geometry("350x300")
root.configure(bg=BG_WHITE)
root.resizable(False, False)

# Header
header = tk.Frame(root, bg=HEADER_BG, height=40)
header.pack(fill=tk.X)
header.pack_propagate(False)
tk.Label(header, text="ChatBot - Online", bg=HEADER_BG, fg=BG_WHITE, font=FONT_HEADER).pack(pady=10)

# Instruction
tk.Label(root, text="Kindly enter your message below to\nsend a request to the server.", bg=BG_WHITE, fg=TEXT_LIGHT, font=FONT_BODY, justify=tk.CENTER).pack(pady=(20, 15))

# Bordered Input Field
input_border = tk.Frame(root, bg=BORDER_COLOR, bd=1)
input_border.pack(padx=20, pady=10, fill=tk.X)
entry_msg = tk.Entry(input_border, font=FONT_BODY, relief=tk.FLAT, bg=BG_WHITE, fg=TEXT_DARK)
entry_msg.pack(padx=5, pady=8, fill=tk.X)
entry_msg.insert(0, "Enter message...")
entry_msg.bind("<FocusIn>", lambda args: entry_msg.delete('0', 'end') if entry_msg.get() == "Enter message..." else None)

# Button
btn_send = tk.Button(root, text="Send Message", command=send_message, bg=HEADER_BG, fg=BG_WHITE, font=("Helvetica", 10, "bold"), relief=tk.FLAT, cursor="hand2")
btn_send.pack(padx=20, pady=15, fill=tk.X, ipady=5)

# Response Label
lbl_response = tk.Label(root, text="", bg=BG_WHITE, fg=TEXT_DARK, font=FONT_BODY)
lbl_response.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()