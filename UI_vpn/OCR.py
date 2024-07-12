import tkinter as tk
import threading
from vpn_server import start_server
from vpn_client import connect_to_server

class SimpleVPNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple VPN Interaction UI")

        self.text = tk.Text(root, height=20, width=80)
        self.text.pack()

        self.start_server_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_server_button.pack()

        self.start_client_button = tk.Button(root, text="Start Client", command=self.start_client)
        self.start_client_button.pack()

    def log_message(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)

    def start_server(self):
        threading.Thread(target=start_server, args=('127.0.0.1', 9999, self.log_message)).start()

    def start_client(self):
        threading.Thread(target=connect_to_server, args=('127.0.0.1', 9999, self.log_message)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleVPNApp(root)
    root.mainloop()
