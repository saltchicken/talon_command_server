import socket
import pyautogui

def recv_all(sock, bufsize=4096):
    """
    Receive data from the socket until no more data is available.
    """
    data = b""
    while True:
        chunk = sock.recv(bufsize)
        if not chunk:
            break
        data += chunk
    return data

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 12345)
print('Starting up on {} port {}'.format(*server_address))
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

while True:
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()
    
    try:
        print('Connection from', client_address)

        received_data = recv_all(connection)
        print('Received {!r}'.format(received_data))

        if received_data == b'minimize window':
            pyautogui.hotkey('win', 'down')
                
    finally:
        # Clean up the connection
        connection.close()