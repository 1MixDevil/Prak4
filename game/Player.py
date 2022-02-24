class Player:

    def __init__(self, count, nick, key):
        self.name = nick
        self.new_shop = {}
        self.balance = 10000
        self.material = 4
        self.plane = 2
        self.shop = 2
        self.live = True
        self.key = key
        self.buy_material = []
        self.sell_plane = []
        self.create_plane = 0

    def sum_taxes(self):
        material_sum = self.material * 300
        plane_sum = self.plane * 500
        shop_sum = self.shop * 1000
        return material_sum + plane_sum + shop_sum

    def add_shop(self):
        if self.shop >= 6:
            return False
        if self.balance < 2500:
            self.live = False
            return False
        self.new_shop = self.new_shop | {self.shop+1: 4}
        self.balance -= 2500
