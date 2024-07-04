from threading import Thread
import socket
import sys

# Server address
server_addr = (socket.gethostbyname(socket.gethostname()), 9999)

# Initialize the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

# Enter client's name
my_name = input('Enter your name: ')
sock.sendto(my_name.encode(), server_addr)
print('Enter destination name and the message: ')
def output_recvfrom(sock):

    while True:
        data, _ = sock.recvfrom(1024)
        if data:
            print(data.decode())


# Start the thread to listen for incoming messages
recv_thread = Thread(target=output_recvfrom, args=(sock, ))
recv_thread.start()

# Read and send messages from standard input
for line in sys.stdin:
    sock.sendto(line.strip().encode(), server_addr)


# Close the socket
sock.close()
recv_thread.join()
