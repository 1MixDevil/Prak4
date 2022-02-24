import requests
from game.Place import Place
from game.Player import Player
from flask import Flask, jsonify, request

Game1 = Place(2)

app = Flask(__name__)


@app.post("/connect")
def connect():
    name = request.json
    key = Game1.generator_key()
    player = Player(Game1.players_live, name["name"], key)
    Game1.players.append(player)
    Game1.key_players = Game1.key_players | {key: player}
    Game1.players_live += 1

    if Game1.players_live == 2:
        ret = Game1.price_this_lvl | {"User_key" : key}
        return jsonify(ret)
    return jsonify(started=False, User_key=key)


@app.get("/fun")
def fun():
    if Game1.players_live == 2:
        return jsonify(Game1.price_this_lvl)
    return jsonify(started=False)

@app.get("/info")
def information():
    return jsonify(Game1.create_info())


@app.post("/finish")
def finish():
    Game1.all_finished += 1
    if Game1.all_finished % len(Game1.players) == 0:
        Game1.produce()
        Game1.start_month()
        Game1.buy_raw(Game1.price_this_lvl["material"])
        Game1.sell_planes(Game1.price_this_lvl["plane"])
        # Game1.taxes()
        return jsonify(Game1.price_this_lvl)

    return jsonify(started=False)

@app.get("/fun_fin")
def fun_fin():
    if Game1.all_finished % len(Game1.players) == 0:
        return jsonify(Game1.price_this_lvl)
    else:
        return jsonify(started=False)


@app.route("/buy_raw", methods=["POST"])
def buy_raw():
    order = request.json
    Game1.key_players[order["key"]].buy_material = [order["count"], order["price"]]
    return jsonify(1)


@app.route("/sell_planes", methods=["POST"])
def sell_planes():
    order = request.json
    Game1.key_players[order["key"]].sell_plane = [order['count'], order["price"]]
    return jsonify(1)


@app.route("/build", methods=["POST"])
def build():
    order = request.json["key"]
    Game1.key_players[order].add_shop()


@app.route("/produce", methods=["POST"])
def produce():
    order = request.json
    Game1.key_players[order["key"]].create_plane += int(order["count"])
    Game1.key_players[order["key"]].balance -= 2000 * int(order["count"])
    Game1.key_players[order["key"]].material -= int(order["count"])
    return jsonify(1)


if __name__ == "__main__":
    app.run()
