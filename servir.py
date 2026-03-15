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

