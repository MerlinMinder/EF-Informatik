import json


def Save(data):
    with open("players.json", "w") as player:
        players = {}
        for key, value in data.items():
            players[key] = vars(value)
            del players[key]["channel"]
        print(players)
        player.write(json.dumps(players, indent=4))
        print("Saved data")


def GetPlayers():
    with open("plyaers.json", "r") as player:
        players = json.load(player)
        print("Loaded data")
        return players
