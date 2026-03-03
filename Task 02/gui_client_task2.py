import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 55555

# --- MINIMALIST STYLE CONSTANTS ---
BG_WHITE = "#FFFFFF"
HEADER_BG = "#222222"
TEXT_DARK = "#333333"
BORDER_COLOR = "#CCCCCC"
FONT_HEADER = ("Helvetica", 11, "bold")
FONT_BODY = ("Helvetica", 10)

# --- GLOBAL VARIABLES ---
client = None
chat_display = None
entry_msg = None

def receive_messages(client_sock, display_widget):
    while True:
        try:
            msg = client_sock.recv(1024).decode('utf-8')
            if msg:
                display_widget.config(state=tk.NORMAL)
                display_widget.insert(tk.END, f"{msg}\n")
                display_widget.config(state=tk.DISABLED)
                display_widget.yview(tk.END)
            else:
                break
        except:
            display_widget.config(state=tk.NORMAL)
            display_widget.insert(tk.END, "Disconnected from server.\n")
            display_widget.config(state=tk.DISABLED)
            break

def send_message(event=None):
    global entry_msg, client, chat_display
    
    msg = entry_msg.get().strip()
    
    if not msg:
        return
        
    if msg.lower() == 'exit':
        client.close()
        root.quit()
        return
    
    try:
        client.send(msg.encode('utf-8'))
        
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {msg}\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        entry_msg.delete(0, tk.END) 
    except:
        messagebox.showerror("Error", "Could not send message.")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Task 2 Chat")
root.geometry("450x500") # Slightly wider
root.configure(bg=BG_WHITE)
root.minsize(400, 400) # Prevents the window from being shrunk too much

# --- NETWORK CONNECTION ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    root.withdraw()
    messagebox.showerror("Error", "Could not connect to server.")
    exit()

# 1. Header (Packed to the TOP)
header = tk.Frame(root, bg=HEADER_BG, height=45)
header.pack(side=tk.TOP, fill=tk.X)
header.pack_propagate(False)
tk.Label(header, text="ChatAPP - Echo Chat", bg=HEADER_BG, fg=BG_WHITE, font=FONT_HEADER).pack(pady=12)

# 2. Input Area (***FIX***: Packed to the BOTTOM first so it never gets cut off)
input_frame = tk.Frame(root, bg=BG_WHITE)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(10, 20))

entry_msg = tk.Entry(input_frame, font=FONT_BODY, bg=BG_WHITE, fg=TEXT_DARK, relief=tk.FLAT, highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor="#888888")
entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
entry_msg.bind("<Return>", send_message)

btn_send = tk.Button(input_frame, text="Send", command=send_message, bg=HEADER_BG, fg=BG_WHITE, font=("Helvetica", 10, "bold"), relief=tk.FLAT, cursor="hand2", activebackground="#444444", activeforeground=BG_WHITE)
btn_send.pack(side=tk.RIGHT, ipadx=15, ipady=4)

# 3. Chat Area (Packed in the remaining middle space)
chat_frame = tk.Frame(root, bg=BG_WHITE, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR)
chat_frame.pack(side=tk.TOP, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Note: Added height=10 to stop ScrolledText from demanding too much vertical space
chat_display = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED, font=FONT_BODY, bg=BG_WHITE, fg=TEXT_DARK, relief=tk.FLAT, padx=10, pady=10, height=10)
chat_display.pack(fill=tk.BOTH, expand=True)

# Start receive thread
recv_thread = threading.Thread(target=receive_messages, args=(client, chat_display))
recv_thread.daemon = True
recv_thread.start()

# Forces the cursor into the box
entry_msg.focus_set()

if __name__ == "__main__":
    root.mainloop()