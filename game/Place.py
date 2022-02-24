import random
from copy import deepcopy

from game.Player import *


class Place:
    def __init__(self, count):
        self.Start_Game = False
        self.count = count
        self.players = []
        self.info = 0
        self.players_live = 0
        self.number_move = 1
        self.now_level = 3
        self.all_finished = 0
        self.key_players = {}
        self.information = {"number_move": self.number_move, "players": [], "last_auction": [], "players_live": count}
        self.chance_level = {1: [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5],
                             2: [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 5],
                             3: [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5],
                             4: [1, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5],
                             5: [1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]}
        self.info_level = {1: [1.0, 800, 3.0, 6500],
                           2: [1.5, 650, 2.5, 6000],
                           3: [2.0, 500, 2.0, 5500],
                           4: [2.5, 400, 1.5, 5000],
                           5: [3.0, 300, 1.0, 4500]}
        self.price_this_lvl = {"started": True, "material": 2*self.count, "size_material": 500, "plane": 2*self.count, "size_plane": 5500}

    def generator_key(self):
        return random.randint(10000000, 999999999)

    def start_month(self):
        self.information = {"number_move": self.number_move, "players": [], "last_auction": [], "players_live": self.count}
        for i in self.players:
            if i.live:
                if len(i.new_shop) != 0:
                    new_dict = {}
                    for j in i.new_shop:
                        date = i.new_shop[j]
                        if date == 0:
                            i.shop += 1
                            if i.balance < 2500:
                                i.live = False
                                i.balance = 0
                                i.plane = 0
                                i.material = 0
                                i.shop = 0
                                break
                            i.balance -= 2500
                        else:
                            i.new_shop[j] -= 1
                            new_dict = new_dict | i.new_shop
                    i.new_shop = new_dict
        self.new_level()
        self.number_move += 1

        return self.price_new_level()

    def produce(self):
        for i in self.players:
            if i.create_plane != 0:
                if i.live:
                    i.plane += i.create_plane
                    i.create_plane = 0

    def create_info(self):
        inf = deepcopy(self.information)
        for i in self.players:
            a = (i.name, i.balance, i.material, i.plane, i.shop, i.live, i.key)
            inf["players"].append(a)

        return inf

    def taxes(self):
        if self.number_move == 0:
            return False
        else:
            for player in self.players:
                if 1:
                    sum = player.sum_taxes()
                    if sum <= player.balance:
                        player.balance -= sum
                    else:
                        player.balance = 0
                        player.plane = 0
                        player.material = 0
                        player.live = False
                        if "leave" not in self.price_this_lvl:
                            self.price_this_lvl = self.price_this_lvl | {"leave":[player.name]}
                        else:
                            self.price_this_lvl["leave"].append(player.name)
                        self.players_live -= 1
                        return False
        return True

    def sell_planes(self, info):
        members = {}
        for i in self.players:
            if len(i.sell_plane) != 0:
                members = members | {int(i.sell_plane[1]): (int(i.sell_plane[0]), i)}
            i.sell_plane = []
        while info != 0:
            if len(members) == 0:
                break
            MIN = min(members)
            count, person = members[MIN]
            if count > info:
                count = info
            if count * MIN <= person.balance:
                info -= count
                person.balance += count * MIN
                person.plane -= count
                del members[MIN]
            else:
                count = person.balance // MIN
                info -= count
                person.balance += count * MIN
                person.plane -= count
                del members[MIN]

    def buy_raw(self, info):
        members = {}
        for i in self.players:
            if len(i.buy_material) != 0:
                members = members | {int(i.buy_material[1]): (int(i.buy_material[0]), i)}
            i.buy_material = []
        while info != 0:
            if len(members) == 0:
                break
            MAX = max(members)
            count, person = members[MAX]
            if count > info:
                count = info

            if count * MAX <= person.balance:
                info -= count
                person.balance -= count * MAX
                person.material += count
                del members[MAX]
            else:
                count = person.balance // MAX
                info -= count
                person.balance -= count * MAX
                person.material += count
                del members[MAX]


    def buy_planes(self):
        pass

    def price_new_level(self):
        info = self.info_level[self.now_level]
        material = info[0] * self.players_live
        plane = info[2] * self.players_live
        self.price_this_lvl = {"material": int(material), "size_material": info[1], "plane": int(plane), "size_plane": info[3], "started": True}
        return self.price_this_lvl

    def new_level(self):
        self.now_level = self.chance_level[self.now_level][random.randint(0, 11)]

    def move(self):
        if self.players[0].live:
            self.taxes()
            self.new_level()

    def status(self):
        pass
