import socket
import base64

def connect_to_server(host='127.0.0.1', port=9999, ui_callback=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    message = base64.b64encode(b"Hello from client!")
    client.send(message)
    ui_callback(f"Client sent: Hello from client!")

    response = client.recv(4096)
    ui_callback(f"Client received: {base64.b64decode(response).decode('utf-8')}")

    client.close()

if __name__ == "__main__":
    def print_callback(message):
        print(message)
    
    connect_to_server(ui_callback=print_callback)
