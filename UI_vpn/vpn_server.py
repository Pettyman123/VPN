import socket
import threading
import base64

def handle_client(client_socket, ui_callback):
    while True:
        try:
            request = client_socket.recv(4096)
            if not request:
                break
            decoded_message = base64.b64decode(request).decode('utf-8')
            ui_callback(f"Server received: {decoded_message}")
            response = base64.b64encode(b"Hello from server!")
            client_socket.send(response)
            ui_callback(f"Server sent: Hello from server!")
        except:
            break

    client_socket.close()

def start_server(host='0.0.0.0', port=9999, ui_callback=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    ui_callback(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        ui_callback(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, ui_callback))
        client_handler.start()

if __name__ == "__main__":
    def print_callback(message):
        print(message)
    
    start_server(ui_callback=print_callback)
