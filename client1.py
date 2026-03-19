import socket
import threading

user_name = "user_1"
password = "123" 
user_name_2 = "user_2"


def connected():
    def receive_messages(sock):
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                print(f"\nСобеседник: {data.decode()}")
                print("Вы: ", end="", flush=True)
            except:
                break

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((socket.gethostname(), 12345))
    except ConnectionRefusedError:
        print("Сервер не запущен!")
        return

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    auth_data = f"{user_name}:{password}"
    client.send(auth_data.encode())
    import time
    time.sleep(1000)
    client.send(user_name.encode())
    while True:
        message = input("Вы: ")
        message = f"{user_name_2},{message}"
        client.send(message.encode())


    client.close()

connected()
