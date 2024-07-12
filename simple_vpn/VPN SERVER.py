import socket 
import threading
import base64

def handle_cleint(client_scoket):
    while True:
        try:
            request = client_scoket.recv(4096)
            if not request:
                break
            decoded_message = base64.b64decode(request).decode('utf-8')
            print(f"Received: {decoded_message}")

            response = base64.b64encode(b"Hello from server side")
            client_scoket.send(response)
        except:
            break
    client_scoket.close()


def start_server(host="0.0.0.0", port = 9999):
    sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sever.bind((host, port))
    sever.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = sever.accept()
        print(f"Client connected from {client_address}")
        client_handler = threading.Thread(target=handle_cleint, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()