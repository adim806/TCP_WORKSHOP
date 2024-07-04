import socket
import threading

# Step 1: Create an array of 5 ports
ports = [5000, 5001, 5002, 5003, 5004]

def handle_client_connection(client_socket, address):
    print(f"New connection from {address}")

    message = client_socket.recv(1024).decode()
    if message == "Hello":
        client_socket.send("World".encode())
    client_socket.close()

def start_server(port_index):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', ports[port_index]))
    server_socket.listen(5)
    print(f"Server listening on port {ports[port_index]}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket, addr))
        client_handler.start()


def connect_to_other_servers(port_index):
    #the loop iterating the servers beside myself(port[port_index])
    for i in range(len(ports)):
        if i == port_index:
            continue
        port = ports[i]
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', port))
            client_socket.send("Hello".encode())
            response = client_socket.recv(1024).decode()
            if response == "World":
                print(f"Connection to port {port} successful: Received 'World'")
            client_socket.close()
        except ConnectionRefusedError:
            print(f"Connection to port {port} failed: No server listening")


if __name__ == "__main__":
    port_index = int(input(f"Choose a port index (0-{len(ports) - 1}): "))

    # Start the server
    server_thread = threading.Thread(target=start_server, args=(port_index,))
    server_thread.start()

    # Connect to other servers
    connect_to_other_servers(port_index)
