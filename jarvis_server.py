import socket
import threading
from loguru import logger

TASKER_PORT = 12345
TALON_PORT = 12346


    
def tasker_thread_handler(server_socket):
    while True:
        logger.debug("Tasker thread waiting for connection")
        conn, addr = server_socket.accept()
        logger.debug(f"Connection from {addr}")
        # while True:
        #     data = conn.recv(1024).decode()
        #     if not data:
        #         break
        conn.close()
    logger.debug('tasker thread done')
    
def talon_thread_handler(server_socket):
    while True:
        logger.debug("Talon thread waiting for connection")
        conn, addr = server_socket.accept()
        logger.debug(f"Connection from {addr}")
        # while True:
        #     data = conn.recv(1024).decode()
        #     if not data:
        #         break
        conn.close()
    logger.debug('talon thread done')

def main():
    tasker_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tasker_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tasker_server_socket.bind(('0.0.0.0', 9998))
    tasker_server_socket.listen(1)
    
    talon_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # talon_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    talon_server_socket.bind(('0.0.0.0', 9999))
    talon_server_socket.listen(1)
    
    tasker_thread = threading.Thread(target=tasker_thread_handler, args=(tasker_server_socket,))
    talon_thread = threading.Thread(target=talon_thread_handler, args=(talon_server_socket,))
    
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