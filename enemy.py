class Enemy(object):
    def __init__(self) -> None:
        self.stats = {"health": 2800, "damagemin": 50,
                      "damagemax": 1000, "coinsmin": 1000, "coinsmax": 1000, "xp": 10000}
        self.type = "dragon"
        self.attack = "burned"
        self.minlevel = 100
