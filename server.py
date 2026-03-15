import socket
import threading
import json
import os

connected = []

if not os.path.exists('data-base.json'):
    with open('data-base.json', 'w') as f:
        json.dump({}, f)

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data: break
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((socket.gethostname(), 12345))
            client.send(data.encode())
            client.close()
        except: break

def connected():
    global connected
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('0.0.0.0', 12345)) 
    server.listen(5)
    print("Ожидание подключения...")
    
    con, addr = server.accept()
    connected.append(addr)
    
    
    raw_data = con.recv(1024).decode()
    if ":" not in raw_data:
        print("Неверный формат данных от клиента")
        return
        
    login, password = raw_data.split(":", 1)

    with open('data-base.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    if login in db:
        if db[login] == password:
            print(f"Пользователь {login} вошел")
            con.send("OK".encode())
        else:
            print("Ошибка пароля")
            con.send("WRONG_PASS".encode())
            con.close()
            return
    else:
        db[login] = password
        with open('data-base.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        print(f"Зарегистрирован новый пользователь: {login}")
        con.send("REGISTERED".encode())

    threading.Thread(target=receive_messages, args=(con,), daemon=True).start()
    

threading.Thread(target=connected, daemon=True).start()