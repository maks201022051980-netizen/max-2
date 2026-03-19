import socket
import threading
import json
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345)) 

conected = {}

def register(raw_data):
        if not os.path.exists('data-base.json'):
            with open('data-base.json', 'w') as f:
                json.dump({}, f)
                
            login, password = raw_data.split(":", 1)

            with open('data-base.json', 'r', encoding='utf-8') as f:
                db = json.load(f)

            if login in db:
                if db[login] == password:
                    print(f"Пользователь {login} вошел")
                    return 1
                else:
                    print("Ошибка пароля")
                    return 2
            else:
                db[login] = password,addr
                with open('data-base.json', 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=4, ensure_ascii=False)
                print(f"Зарегистрирован новый пользователь: {login}")
                return 1

def lisen_register(con):
            mesage = con.recv(1024).decode()
            register(mesage)
            if register == 2:   return False
            else: return True
def push(Soket_Client1):
        global conected
        user2,mesage = (Soket_Client1.recv(1024).decode()).split(",")
        Soket_Client2 = conected[user2]
        Soket_Client2.send(mesage.decode())


def connected(Soket_Client1):
        global conected
        user = (Soket_Client1.recv(1024).decode()).split(",")
        conected = {user : Soket_Client1}


while True:
        server.listen(5)
        Soket_Client1, addr = server.accept()
        if lisen_register(Soket_Client1) == False:
            Soket_Client1.close()
        connected(Soket_Client1)
        threading.Thread(target=push, args=(Soket_Client1), daemon=True).start()


import socket
import threading
import json
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345)) 

conected = []

def register(raw_data):
        if not os.path.exists('data-base.json'):
            with open('data-base.json', 'w') as f:
                json.dump({}, f)
                
            login, password = raw_data.split(":", 1)

            with open('data-base.json', 'r', encoding='utf-8') as f:
                db = json.load(f)

            if login in db:
                if db[login] == password:
                    print(f"Пользователь {login} вошел")
                    return 1
                else:
                    print("Ошибка пароля")
                    return 2
            else:
                db[login] = password,addr
                with open('data-base.json', 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=4, ensure_ascii=False)
                print(f"Зарегистрирован новый пользователь: {login}")
                return 1

def lisen_register(con,addr):
            mesage = con.recv(1024).decode()
            register(mesage)
            if register == 2:   return False
            conected.append(addr)


def otpravit(con2,mesage):
            con2.send(mesage).encode()

while True:
        con, addr = server.accept()
        if lisen_register(con, addr) != True: con.close()

