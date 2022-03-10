import time
import os
import requests

def finish():
    rec = requests.post(f"http://{ip}:5000/finish")
    if not rec.json()["started"]:
        num = 0
        while 1:
            num += 1
            if num >= 3:
                num = 0
            gest = requests.get(f"http://{ip}:5000/fun_fin")
            if gest.json()["started"]:
                break
            c = ["Wait.  ", "Wait.. ", "Wait..."]
            print(c[num], end= '\r')
            time.sleep(1)
        if "leave" in gest.json():
            for i in gest.json()["leave"]:
                print(f"{i} выбыл")
                time.sleep(2)
        return gest.json()
    if "leave" in rec.json():
        for i in rec.json()["leave"]:
            print(f"{i} выбыл")
            time.sleep(2)
    return rec.json()


def build():
    answer = input(f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n"
                   "Введите 'stop', если хотите отменить, и что-то другое, если хотите продолжить операцию \n"
                   "Строительство вам обойдётся в 5000р, причем сначала спишется только 2500, и еще 2500 в конце\n"
                   "Строительство займет 4 месяца \n")
    clear()
    if answer == "stop":
        return False

    order = {
        "key": key,
    }
    rec = requests.post(f"http://{ip}:5000/build", json=order)


def info():
    rec = requests.get(f"http://{ip}:5000/info").json()
    print(f"Сейчас идёт {rec['number_move']} месяц")
    print("Живые игроки:")
    for i in rec["players"]:
        if not i[5]:
            print(f"Игрок {i[0]} выбыл :(")
        else:
            print(
                f"Имя: {i[0]}, баланс: {i[1]} рублей, количество сырья: {i[2]} шт, количество самолётов: {i[3]} шт, количество цехов: {i[4]} шт")
    print("\n \n")


def buy_raw():
    answer = input(f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n"
                   "Введите 'stop', если хотите отменить, и что-то другое, если хотите продолжить операцию \n")
    clear()
    if answer == "stop":
        return False

    print(f"Сегодня ты можешь купить {gest['material']} единиц сырья \n"
          f"По минимальной цене в {gest['size_material']} рублей \n"
          f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья")
    count = input("Введи количество сырья, которое хочешь купить: \n")
    while 1:
        if 1 > int(count) > gest["material"]:
            count = input(
                f"Вы ввели неправильное количество сырья, проверьте, оно не должно быть нулём, и должно быть меньше {gest['material']}: \n")
        else:
            break
    money = input(
        f"Введи, какую сумму денег ты готов отдать за единицу сырья {gest['size_material']} минимум, у тебя есть {information[1]}\n")
    while 1:
        if int(gest["size_material"]) > int(money):
            money = input(
                f"Вы ввели неправильное кол-во денег, проверьте, что данная сумма есть у вас на балансе и она не меньше, чем {gest['size_material']}, у тебя есть {information[1]}рублей, на балансе \n")
        else:
            break
    order = {
        "count": count,
        "price": money,
        "key": key
    }
    rec = requests.post(f"http://{ip}:5000/buy_raw", json=order)


def sell_planes():
    answer = input(f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n"
                   "Введите 'stop', если хотите отменить, и что-то другое, если хотите продолжить операцию \n")
    clear()
    if answer == "stop":
        return False

    count = input(
        f"Сегодня ты можешь продать банку *точка* {gest['plane']} самолётов, сколько самолётов ты хочешь продать, у тебя есть {information[3]}: \n")
    while 1:
        try:
            if 1 > int(count) > gest['plane']:
                count = input(
                    f"Проверь, правильное ли число ты ввёл, оно должно быть меньше {gest['plane']}, но больше 0, у тебя есть {information[4]}")
            else:
                if int(count) <= information[3]:
                    break
        except ValueError():
            count = input(
                f"Проверь, правильное ли число ты ввёл, оно должно быть меньше {gest['plane']}, но больше 0, у тебя есть {information[3]}")

    money = input(
        f"Банк может купить у тебя самолёт, максимум за {gest['size_plane']} р, за сколько продашь один самолёт: \n")
    while 1:
        try:
            if gest["size_plane"] < int(money):
                money = input(f"Проверь, правильно ли число ты ввёл, оно должно быть не больше {gest['size_plane']}")
            else:
                break
        except ValueError():
            money = input(f"Проверь, правильно ли число ты ввёл, оно должно быть не больше {gest['size_plane']}")

    order = {
        "key": key,
        "count": count,
        "price": money,
    }
    resp = requests.post(f"http://{ip}:5000/sell_planes", json=order)


def print_inf():
    print(f"\nВот цены на сегодня: \n"
          f"    Предложений сырья: {gest['material']} \n"
          f"    Минимальная цена сырья: {gest['size_material']} \n"
          f"    Спрос на истребители: {gest['plane']} \n"
          f"    Максимальная цена за истребитель: {gest['size_plane']} т.р. \n")


def produce():
    answer = input(f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n"
                   "Введите 'stop', если хотите отменить, и что-то другое, если хотите продолжить операцию \n")
    clear()
    if answer == "stop":
        return False

    count = input(f"Сколько самолётов вы бы хотели сегодня произвести, максимум {information[4]} штуки\n"
                  f"Цена за один самолёт 2000р и одна единица сырья, \n"
                  f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n")
    while i:
        if int(count) <= information[4]:
            break
        else:
            count = input(
                f"Проверьте, сколько вы хотите произвести сегодня самолётов, максимум {information[4]} штуки\n"
                f"Цена за один самолёт 2000р и одна единица сырья, \n"
                f"у тебя есть {information[1]} рублей и {information[2]} единиц сырья \n")
    json = {
        "key": key,
        "count": count,
    }
    resp = requests.post(f"http://{ip}:5000/produce", json=json)


clear = lambda: os.system('clear')

# name = input("Введите имя: \n")
name = input("Введите ник игрока: \n")
check = {
    "name": name,
    "room": 1
}
ip = "192.168.1.200"

resp = requests.post(f"http://{ip}:5000/connect", json=check)
key = resp.json()["User_key"]
numb = 0
while 1:
    numb += 1
    if numb >= 3:
        numb = 0
    gest = requests.get(f"http://{ip}:5000/fun")
    if gest.json()["started"]:
        break
    c = ["Wait.  ", "Wait.. ", "Wait..."]
    print(c[numb], end='\r')
    time.sleep(1)
    # ТУУУУТ

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
    information = requests.get(f"http://{ip}:5000/info").json()
    players_live = 0
    for i in information["players"]:
        if i[5]:
            players_live += 1
    if players_live <= 1:
        break
    for i in information["players"]:
        if i[6] == key:
            information = i
            break
    clear()
    answer = 0
    c = ["info", "buy_raw", "sell_planes", "produce", "build", "finish"]
    ca = {"info": "Получить информацию об игре ",
          "buy_raw": "Поучаствовать в акции на сырьё",
          "sell_planes": "Поучаствовать в акции на продукцию",
          "produce": "производство самолёта",
          "build": "Построить новый цех",
          "finish": "закончить данный месяц"}
    while answer != "finish":
        print_inf()

        for i in c:
            print(f"{i} {ca[i]}")
        answer = input()
        clear()
        if answer not in c:
            print("\nВы ввели что-то неправильно или уже выполняли данное действие, в этом месяце \n")
        else:
            c.remove(answer)
            a = move[answer]()
    gest = a

for i in information["players"]:
    if i[5] == True:
        print(f"{i[0]} выиграл")
