import socket
import threading
import logging

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = set()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


def broadcast(message, sender) -> None:
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except Exception as e:
                print(f'Error: {type(e).__name__}, {e}')
                logging.exception(e)
                clients.remove(client)


def handle(client) -> None:
    while True:
        try:
            message = client.recv(1024)
            if b'q' == message:
                logging.info(f'Client disconnected: {client.getpeername()}')
                clients.remove(client)
                # client.close()
                break

            logging.info(f'client {client.getpeername()} sent {message}')
            broadcast(message, client)
        except Exception as e:
            print(f'Error: {type(e).__name__}, {e}')
            logging.exception(e)
            break


def receive() -> None:
    while True:
        client, address = server.accept()
        logging.info(f'Client connected: {address}')
        clients.add(client)

        client.send('Connected to the server'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server starting...')
receive()
