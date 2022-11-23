import json
from Player import Player

"""
Saves and loads the Player() objects of each member in the server
"""


def getPlayers(members) -> dict:
    """loads all values from json and assigns them to members"""

    returnplayers = {}
    with open("players.json", "r") as playersjson:
        playerdata = json.load(playersjson)
    # loop over player data
    for player in playerdata:
        # loop over members and check if member name == player name
        # if true member has save a character and it is re-created
        for member in members:
            if player["name"] == member.name:
                returnplayers[member] = Player(player["name"], stats=player["stats"], gear=player["gear"],
                                               equipment=player["equipment"], attacktype=player['attacktype'], classtype=player['classtype'])

    # returns object of all members and corresponding Player() objects
    return returnplayers


def savePlayers(data) -> None:
    """saves essential values of players into json file"""

    with open("players.json", "w") as player:
        players = []
        # loop over each player
        # key = name, value = Player() object
        for key, value in data.items():
            values = {}
            # loop over all variables in Player() object
            # key2 = variable name, value2 = variable value
            for key2, value2 in vars(value).items():
                # do not include channel or enemy objects
                # (they can't be saved in json)
                if key2 != "channel" and key2 != "enemy":
                    values[key2] = value2
            players.append(values)

        player.write(json.dumps(list(players), indent=4))
        print("Saved data")

    return None
