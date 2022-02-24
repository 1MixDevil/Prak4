import time
import os
import requests


def finish():
    rec = requests.post("http://127.0.0.1:5000/finish")
    if not rec.json()["started"]:
        while 1:
            gest = requests.get("http://127.0.0.1:5000/fun_fin")
            if gest.json()["started"]:
                break
            time.sleep(1)
            print("Wait...")
        if "leave" in gest.json():
            for i in gest.json()["leave"]:
                clear()
                print(f"{i} выбыл")
        return gest.json()
    if "leave" in rec.json():
        for i in rec.json()["leave"]:
            clear()
            print(f"{i} выбыл")
    return rec.json()


def build():
    order = {
        "key": key,
    }
    rec = requests.post("http://127.0.0.1:5000/build", json=order)


def info():
    rec = requests.get("http://127.0.0.1:5000/info").json()
    print(f"Сейчас идёт {rec['number_move']} месяц")
    print("Живые игроки:")
    for i in rec["players"]:
        if not i[5]:
            print(f"Игрок {i[0]} выбыл :(")
        else:
            print(f"Имя: {i[0]}, баланс: {i[1]} рублей, количество сырья: {i[2]} шт, количество самолётов: {i[3]} шт, количество цехов: {i[4]} шт")
    print("\n \n")


def buy_raw():
    print(f"Сегодня ты можешь купить {gest['material']} единиц сырья \n" 
          f"По минимальной цене в {gest['size_material']} рублей \n"
          f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья")
    count = input("Введи количество сырья, которое хочешь купить: \n")
    while 1:
        if 1 > int(count) > gest["material"]:
            count = input(f"Вы ввели неправильное количество сырья, проверьте, оно не должно быть нулём, и должно быть меньше {gest['material']}: \n"
                          f"")
        else:
            break
    money = input(f"Введи, какую сумму денег ты готов отдать за единицу сырья {gest['size_material']} минимум, у тебя есть {information[1]}\n")
    while 1:
        if int(gest["size_material"]) > int(money):
            money = input(f"Вы ввели неправильное кол-во денег, проверьте, что данная сумма есть у вас на балансе и она не меньше, чем {gest['size_material']}, у тебя есть {information[1]}рублей, на балансе \n")
        else:
            break
    order = {
        "count": count,
        "price": money,
        "key": key
    }
    rec = requests.post("http://127.0.0.1:5000/buy_raw", json=order)


def sell_planes():
    count = input(f"Сегодня ты можешь продать банку *точка* {gest['plane']} самолётов, сколько самолётов ты хочешь продать, у тебя есть {information[4]}: \n")
    while 1:
        if 1 > int(count) > gest['plane']:
            count = input(f"Проверь, правильное ли число ты ввёл, оно должно быть меньше {gest['plane']}, но больше 0, у тебя есть {information[4]}")
        else:
            if int(count) <= information[4]:
                break
    money = input(f"Банк может купить у тебя самолёт, максимум за {gest['size_plane']} р, за сколько продашь один самолёт: \n")
    while 1:
        if gest["size_plane"] < int(money):
            money = input(f"Проверь, правильно ли число ты ввёл, оно должно быть не больше {gest['size_plane']}")
        else:
            break

    order = {
        "key": key,
        "count": count,
        "price": money,
    }
    resp = requests.post("http://127.0.0.1:5000/sell_planes", json=order)


def print_inf():
    print(f"Вот цены на сегодня: \n"
          f"    Предложений сырья: {gest['material']} \n"
          f"    Минимальная цена сырья: {gest['size_material']} \n"
          f"    Спрос на истребители: {gest['plane']} \n"
          f"    Максимальная цена за истребитель: {gest['size_plane']} т.р. \n")

def produce():
    count = input(f"Сколько самолётов вы бы хотели сегодня произвести, максимум {information[4]} штуки\n"
                  f"Цена за один самолёт 2000р и одна единица сырья, \n"
                  f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n")
    while i:
        if int(count) <= information[4]:
            break
        else:
            count = input(f"Проверьте, сколько вы хотите произвести сегодня самолётов, максимум {information[4]} штуки\n"
                          f"Цена за один самолёт 2000р и одна единица сырья, \n"
                          f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n")
    json = {
        "key": key,
        "count": count,
    }
    resp = requests.post("http://127.0.0.1:5000/produce", json=json)

clear = lambda: os.system('cls')

# name = input("Введите имя: \n")
name = input("Введите ник игрока: \n")
check = {
    "name": name,
    "room": 1
}

resp = requests.post("http://127.0.0.1:5000/connect", json=check)
key = resp.json()["User_key"]
while 1:
    gest = requests.get("http://127.0.0.1:5000/fun")
    if gest.json()["started"]:
        break
    time.sleep(1)
    print("Wait...")

clear()
gest = gest.json()
move = {
    "info": info,
    "buy_raw": buy_raw,
    "sell_planes": sell_planes,
    "produce": produce,
    "build": build,
    "finish": finish,
}
while 1:
    information = requests.get("http://127.0.0.1:5000/info").json()
    if information["players_live"] <= 1:
        break
    for i in information["players"]:
        if i[6] == key:
            information = i
            break
    clear()
    answer = 0
    c = ["info", "buy_raw", "sell_planes", "produce", "build", "finish"]
    while answer != "finish":
        print_inf()
        answer = input("Введите, что хотите сделать: \n"
                       "info - Получить информацию об игре \n"
                       "buy_raw - Поучаствовать в акции на сырьё \n"
                       "sell_planes - Поучаствовать в акции на продукцию \n"
                       "produce - производство самолёта\n"
                       "build - Построить новый цех\n"
                       "finish - закончить данный месяц \n")
        clear()
        if answer not in c:
            print("Вы ввели что-то неправильно или уже выполняли данное действие, в этом месяце")
        else:
            c.remove(answer)
            a = move[answer]()
    gest = a

for i in information["players"]:
    if i[5] == True:
        print(f"{i.name} выиграл")