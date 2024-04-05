import socket
import threading
from loguru import logger
import json
import queue
    
def tasker_thread_handler(server_socket, task_queue):
    while True:
        logger.debug("Tasker thread waiting for connection")
        conn, addr = server_socket.accept()
        logger.debug(f"Connection from {addr}")
        while True:
            # data = conn.recv(1024).decode()
            data = task_queue.get()
            if not data:
                break
            packet = json.loads(data)
            print(packet)
        conn.close()
    logger.debug('tasker thread done')
    
def talon_thread_handler(server_socket, task_queue):
    while True:
        logger.debug("Talon thread waiting for connection")
        conn, addr = server_socket.accept()
        logger.debug(f"Connection from {addr}")
        while True:
            data = conn.recv(4096).decode()
            if not data:
                logger.error('Nothing was received. Critical error in talon socket receive')
                break
            else:
                packet = json.loads(data)
                if packet.type == 'phrase':
                    task_queue.put(data)
                else:
                    logger.debug('This packet type has not been implemented yet')
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
    
    task_queue = queue.Queue()
    
    tasker_thread = threading.Thread(target=tasker_thread_handler, args=(tasker_server_socket, task_queue))
    talon_thread = threading.Thread(target=talon_thread_handler, args=(talon_server_socket, task_queue))
    
    # Start the threads
    tasker_thread.start()
    talon_thread.start()

    # Wait for the threads to finish
    tasker_thread.join()
    talon_thread.join()

    # Close the server socket
    tasker_server_socket.close()
    talon_server_socket.close()



# Start the server
if __name__ == "__main__":
    main()
    logger.debug('Quitting out of main')