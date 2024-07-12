import socket
import base64

def connect_to_server(host='127.0.0.1', port = 9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    message = base64.b64encode(b"Hello from client")
    client.send(message)

    response = client.recv(4096)
    print(f"Received: {base64.b64decode(response).decode('utf-8')}")

    client.close()

if __name__ == '__main__':
    connect_to_server()