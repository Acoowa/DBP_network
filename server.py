import socket
import threading
import logging

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")


def broadcast(message, current_client=None) -> None:
    for client in clients:
        if client == current_client or message == ':q':
            continue
        if current_client is None:
            continue

        client.send(message)


def handle(client) -> None:
    while True:
        try:
            message = client.recv(1024)
            logging.info(f'client {clients[client]} got {message}')
            broadcast(message, client)
        except Exception as e:
            print(f'Error: {type(e).__name__}, {e}')
            broadcast(f'Client disconnected: {clients[client]}'.encode())
            del clients[client]
            client.close()
            exit()


def receive() -> None:
    while True:
        client, address = server.accept()
        print(f'New client connected: {str(address)}')

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        clients[client] = nickname

        print(f'Client connected: {nickname}')
        broadcast(f'New client connected: {nickname}'.encode())
        client.send('Connected to the server'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print('Server starting...')
receive()

