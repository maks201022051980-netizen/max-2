import socket
import threading
import json
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 12345))
server.listen(5)  #

conected = {}


def register(raw_data, addr):
    if not os.path.exists('data-base.json'):
        with open('data-base.json', 'w') as f:
            json.dump({}, f)

    try:
        login, password = raw_data.split(":", 1)
    except ValueError:
        print("Вот тут")
        return 2

    with open('data-base.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    if login in db:
        if db[login][0] == password:
            print(f"Пользователь {login} вошел")
            return 1
        else:
            print("И тут")
            return 2

    else:
        db[login] = [password, str(addr)]
        with open('data-base.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        return 1


def lisen_register(con, addr):
    mesage = con.recv(1024).decode()
    res = register(mesage, addr)
    return res == 1


def push(Soket_Client1):
    global conected
    while True:
        try:
            data = Soket_Client1.recv(1024).decode()
            if not data: break
            user2, mesage = data.split(",", 1)
            if user2 in conected:
                Soket_Client2 = conected[user2]
                Soket_Client2.send(mesage.encode())
        except:
            break


def connected(Soket_Client1):
    global conected
    data = Soket_Client1.recv(1024).decode()
    user = data.split(",")[0]
    conected[user] = Soket_Client1
    return user


while True:
    Soket_Client1, addr = server.accept()
    if not lisen_register(Soket_Client1, addr):
        Soket_Client1.send("Error".encode())
        Soket_Client1.close()
        continue

    user_id = connected(Soket_Client1)
    threading.Thread(target=push, args=(Soket_Client1,), daemon=True).start()
