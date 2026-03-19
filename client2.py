import socket
import threading



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
    client.connect((socket.gethostname(), 12345))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True 
    thread.start()

    while True:
        message = input("Вы: ")
        if message.lower() == 'exit':
            break
        client.send(message.encode())

    client.close()
