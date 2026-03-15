import socket
import threading

user_name = "user_1"
password = "123" 
user_name_2 = "user_2"


def connected():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((socket.gethostname(), 12345))
    except ConnectionRefusedError:
        print("Сервер не запущен!")
        return

    auth_data = f"{user_name}:{password}"
    client.send(auth_data.encode())

    
    while True:
        message = input("Вы: ")
        if message.lower() == 'exit':
            break
        if message.strip():
            client.send(message.encode())

    client.close()

connected()
