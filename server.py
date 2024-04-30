import socket
import threading
import logging

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


def broadcast(message, sender) -> None:
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f'Error: {type(e).__name__}, {e}')
                del clients[client]


def handle(client) -> None:
    while True:
        try:
            message = client.recv(1024)
            if message.decode() == ':q':
                broadcast(f'Client disconnected: {clients[client]}'.encode(), client)
                logging.info(f'Client disconnected: {clients[client]}')
                del clients[client]
                client.close()
                continue

            logging.info(f'client {clients[client]} sent {message}')
            broadcast(message, client)
        except Exception as e:
            print(f'Error: {type(e).__name__}, {e}')
            break


def receive() -> None:
    while True:
        client, address = server.accept()
        print(f'New client connected: {str(address)}')

        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        clients[client] = nickname

        print(f'Client connected: {nickname}')
        broadcast(f'New client connected: {nickname}'.encode(), client)
        client.send('Connected to the server'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server starting...')
receive()
