import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox

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

# --- GLOBAL VARIABLES ---
# Pre-defining these so they are accessible everywhere
global_username = ""
client = None
chat_display = None
entry_msg = None

def receive_messages(client_sock, display_widget):
    while True:
        try:
            message = client_sock.recv(1024).decode('utf-8')
            if not message:
                break
            try:
                msg_json = json.loads(message)
                sender = msg_json.get('sender')
                text = msg_json.get('text')
                
                display_widget.config(state=tk.NORMAL)
                display_widget.insert(tk.END, f"{sender}: {text}\n")
                display_widget.config(state=tk.DISABLED)
                display_widget.yview(tk.END)
            except json.JSONDecodeError:
                pass
        except:
            break

def send_message(event=None):
    global chat_display, entry_msg, client, global_username
    
    user_input = entry_msg.get().strip()
    if not user_input or user_input == "Type your message...":
        return

    if user_input.lower() == 'exit':
        client.close()
        root.quit()
        return

    # Original JSON Protocol Logic (Unchanged)
    if ":" in user_input:
        target_user, text_content = user_input.split(":", 1)
        json_packet = {
            "status": "1",
            "sender": global_username,
            "receiver": target_user.strip(),
            "text": text_content.strip()
        }
        client.send(json.dumps(json_packet).encode('utf-8'))
        
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You (to {target_user.strip()}): {text_content.strip()}\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        entry_msg.delete(0, tk.END)
    else:
        messagebox.showwarning("Format Error", "Use format 'Recipient: Message'")

def start_chat():
    global global_username, client
    username = entry_name.get().strip()
    
    if not username or username == "Your Name":
        messagebox.showwarning("Required", "Please enter your name.")
        return

    global_username = username
    
    # Original Connection Logic
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.send(username.encode('utf-8'))
    except:
        messagebox.showerror("Error", "Could not connect to server.")
        return

    # Destroy login widget, build chat widget
    login_frame.destroy()
    build_chat_interface()

def build_chat_interface():
    global chat_display, entry_msg, client
    
    root.geometry("450x550")
    
    header = tk.Frame(root, bg=HEADER_BG, height=45)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    tk.Label(header, text=f"ChatBot - {global_username}", bg=HEADER_BG, fg=BG_WHITE, font=FONT_HEADER).pack(pady=12)

    chat_frame = tk.Frame(root, bg=BORDER_COLOR, bd=1)
    chat_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
    
    # We assign the global variable here
    chat_display = scrolledtext.ScrolledText(chat_frame, state=tk.DISABLED, font=FONT_BODY, bg=BG_WHITE, fg=TEXT_DARK, relief=tk.FLAT, padx=10, pady=10)
    chat_display.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Format: 'Recipient: Message' | Type 'exit' to leave\n----------------------------------------\n")
    chat_display.config(state=tk.DISABLED)

    input_frame = tk.Frame(root, bg=BG_WHITE)
    input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    input_border = tk.Frame(input_frame, bg=BORDER_COLOR, bd=1)
    input_border.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # We assign the global variable here
    entry_msg = tk.Entry(input_border, font=FONT_BODY, relief=tk.FLAT, bg=BG_WHITE, fg=TEXT_DARK)
    entry_msg.pack(padx=5, pady=8, fill=tk.BOTH, expand=True)
    entry_msg.bind("<Return>", send_message)
    
    # Auto-focus the typing cursor so it's ready immediately
    entry_msg.focus()

    btn_send = tk.Button(input_frame, text="Send", command=send_message, bg=HEADER_BG, fg=BG_WHITE, font=("Helvetica", 10, "bold"), relief=tk.FLAT, cursor="hand2")
    btn_send.pack(side=tk.RIGHT, ipadx=15, ipady=4)

    recv_thread = threading.Thread(target=receive_messages, args=(client, chat_display))
    recv_thread.daemon = True
    recv_thread.start()

# --- GUI INITIALIZATION ---
root = tk.Tk()
root.title("Task 3 Chat")
root.geometry("380x280") 
root.configure(bg=BG_WHITE)
root.resizable(False, False)

# --- LOGIN FORM ---
login_frame = tk.Frame(root, bg=BG_WHITE)
login_frame.pack(fill=tk.BOTH, expand=True)

header = tk.Frame(login_frame, bg=HEADER_BG, height=45)
header.pack(fill=tk.X)
header.pack_propagate(False)
tk.Label(header, text="ChatBot - Online", bg=HEADER_BG, fg=BG_WHITE, font=FONT_HEADER).pack(pady=12)

tk.Label(login_frame, text="Kindly enter your name below to begin\nchatting with the next available agent.", bg=BG_WHITE, fg=TEXT_LIGHT, font=FONT_BODY, justify=tk.CENTER).pack(pady=(20, 15))

f1 = tk.Frame(login_frame, bg=BORDER_COLOR, bd=1)
f1.pack(padx=30, pady=10, fill=tk.X)
entry_name = tk.Entry(f1, font=FONT_BODY, relief=tk.FLAT, bg=BG_WHITE, fg=TEXT_DARK)
entry_name.pack(padx=8, pady=10, fill=tk.X)
entry_name.insert(0, "Your Name")
entry_name.bind("<FocusIn>", lambda args: entry_name.delete('0', 'end') if entry_name.get() == "Your Name" else None)

# Auto-focus the login input box so you don't have to click it
entry_name.focus()

btn_start = tk.Button(login_frame, text="Start Chat", command=start_chat, bg=HEADER_BG, fg=BG_WHITE, font=("Helvetica", 11, "bold"), relief=tk.FLAT, cursor="hand2")
btn_start.pack(padx=30, pady=20, fill=tk.X, ipady=8)

if __name__ == "__main__":
    root.mainloop()