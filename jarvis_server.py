import socket
import threading
from loguru import logger

TASKER_PORT = 12347
TALON_PORT = 12346

def talon_thread_handler(server_socket):
    conn, addr = server_socket.accept()
    logger.debug(f"Connection from {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
    conn.close()
    
def tasker_thread_handler(server_socket):
    conn, addr = server_socket.accept()
    logger.debug(f"Connection from {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(2)  # Listen for up to 2 connections
    
    tasker_thread = threading.Thread(target=tasker_thread_handler, args=(server_socket,))
    talon_thread = threading.Thread(target=talon_thread_handler, args=(server_socket,))

    # print("Server is listening for connections...")

    # # Accept connections from two clients
    # client1_conn, client1_addr = server_socket.accept()
    # print(f"Accepted connection from {client1_addr}")
    # client2_conn, client2_addr = server_socket.accept()
    # print(f"Accepted connection from {client2_addr}")

    # Assign variables based on IP addresses
    # if client1_addr[0] == "192.168.1.100":  # Example IP address for tasker
    #     tasker_conn = client1_conn
    #     writer_conn = client2_conn
    # else:
    #     tasker_conn = client2_conn
    #     writer_conn = client1_conn

    # Create threads to handle each client
    

    # Start the threads
    tasker_thread.start()
    talon_thread.start()

    # Wait for the threads to finish
    tasker_thread.join()
    talon_thread.join()

    # Close the server socket
    server_socket.close()



# Start the server
if __name__ == "__main__":
    main()
    logger.debug('Quitting out of main')