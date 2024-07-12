from flask import Flask, render_template, request, jsonify
import threading
import socket
import base64

app = Flask(__name__)

log_messages = []

def log_message(message):
    log_messages.append(message)

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(4096)
            if not request:
                break
            decoded_message = base64.b64decode(request).decode('utf-8')
            log_message(f"Server received: {decoded_message}")
            response = base64.b64encode(b"Hello from server!")
            client_socket.send(response)
            log_message(f"Server sent: Hello from server!")
        except:
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 0))  # Bind to an available port
    port = server.getsockname()[1]
    log_message(f"Server listening on localhost:{port}")

    def server_thread():
        server.listen(5)
        while True:
            client_socket, addr = server.accept()
            log_message(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    
    threading.Thread(target=server_thread).start()
    return port

def start_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))

    message = base64.b64encode(b"Hello from client!")
    client.send(message)
    log_message(f"Client sent: Hello from client!")

    response = client.recv(4096)
    log_message(f"Client received: {base64.b64decode(response).decode('utf-8')}")

    client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_server', methods=['POST'])
def start_server_endpoint():
    port = start_server()
    return jsonify({"status": "Server started", "port": port})

@app.route('/start_client', methods=['POST'])
def start_client_endpoint():
    data = request.json
    port = data.get('port')
    threading.Thread(target=start_client, args=(port,)).start()
    return jsonify({"status": "Client started"})

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(log_messages)

if __name__ == "__main__":
    app.run(debug=True)
