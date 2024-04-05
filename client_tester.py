import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Specify the local address and port
local_address = '0.0.0.0'  # Localhost IP address
local_port = 12350  # Example port number

# Bind the socket to the local address and port
client_socket.bind((local_address, local_port))

# Connect to a remote server
server_address = '192.168.1.11'
server_port = 9999
client_socket.connect((server_address, server_port))
client_socket.close()