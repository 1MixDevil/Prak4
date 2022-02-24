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
        return gest.json()
    return rec.json()


def sell_planes():
    rec = requests.post("http://127.0.0.1:5000/sell_plane")


def produce():
    rec = requests.post("http://127.0.0.1:5000/produce")


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
          f"По минимальной цене в {gest['size_material']} рублей")
    count = input("Введи количество сырья, которое хочешь купить: \n")
    while 1:
        if 1 > int(count) > gest["material"]:
            count = input(f"Вы ввели неправильное количество сырья, проверьте, оно не должно быть нулём, и должно быть меньше {gest['material']}: \n")
        else:
            break
    money = input(f"Введи, какую сумму денег ты готов отдать за единицу сырья {gest['size_material']} минимум \n")
    while 1:
        if int(gest["size_material"]) > int(money):
            money = input(f"Вы ввели неправильное кол-во денег, проверьте, что данная сумма есть у вас на балансе и она не меньше, чем {gest['size_material']} \n")
        else:
            break
    order = {
        "count": count,
        "price": money,
        "key": key
    }
    rec = requests.post("http://127.0.0.1:5000/buy_raw", json=order)


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
while 1:
    clear()
    print(f"Вот цены на сегодня: \n"
          f"    Предложений сырья: {gest['material']} \n"
          f"    Минимальная цена сырья: {gest['size_material']} \n"
          f"    Спрос на истребители: {gest['plane']} \n"
          f"    Максимальная цена за истребитель: {gest['size_plane']} т.р. \n"
          f"Нажмите enter, чтоб продолжить \n")
    input()
    print("\n \n")
    move = {
        "info": info,
        "buy_raw": buy_raw,
        "sell_planes": sell_planes,
        "produce": produce,
        "build": build,
        "finish": finish,

    }
    answer = 0
    while answer != "finish":
        answer = input("Введите, что хотите сделать: \n"
                       "info - Получить информацию об игре \n"
                       "buy_raw - Поучаствовать в акции на сырьё \n"
                       "sell_planes - Поучаствовать в акции на продукцию \n"
                       "produce - производство самолёта\n"
                       "build - Построить новый цех\n"
                       "finish - закончить данный месяц \n")
        clear()
        if answer not in ["info", "buy_raw", "sell_planes", "produce", "build", "finish"]:
            print("Вы ввели что-то неправильно")
        else:
            a = move[answer]()
    gest = a

# inf = requests.get("http://127.0.0.1:5000/info")
# print("Наши игроки:")
# for i in inf.json()["players"]:
#     print(*i)
# clear()

# finish = requests.post("http://127.0.0.1:5000/finish", json=check)
# while 1:
#     gest = requests.get("http://127.0.0.1:5000/fun_fin")
#     if gest.json()["started"]:
#         break
#     time.sleep(1)
