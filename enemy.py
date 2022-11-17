class Enemy(object):
    def __init__(self) -> None:
        self.stats = {"health": 2800, "damagemin": 50,
                      "damagemax": 1000, "coinsmin": 1000, "coinsmax": 1000, "xp": 10000}
        self.type = "dragon"
        self.attack = "burned"
        self.minlevel = 100


ENEMYS = {"dragon": {"type": "dragon", "minlevel": 100, "attack": "burned", "stats": {"health": 2800, "damagemin": 50, "damagemax": 1000, "coinsmin": 1000, "coinsmax": 1000, "xp": 10000}},
          "Minotaur": {"type": "Minotaur", "minlevel": 80, "attack": "charged at", "stats": {"health": 700, "damagemin": 120, "damagemax": 501, "coinsmin": 140, "coinsmax": 140, "xp": 1650}},
          "Orc": {"type": "Orc", "minlevel": 60, "attack": "slammed", "stats": {"health": 1000, "damagemin": 189, "damagemax": 214, "coinsmin": 75, "coinsmax": 110, "xp": 1400}},
          "Banidt": {"type": "Bandit", "minlevel": 40, "attack": "shanked", "stats": {"health": 350, "damagemin": 82, "damagemax": 91, "coinsmin": 30, "coinsmax": 90, "xp": 1150}},
          "Dwarf": {"type": "Dwarf", "minlevel": 25, "attack": "mined", "stats": {"health": 185, "damagemin": 21, "damagemax": 28, "coinsmin": 20, "coinsmax": 28, "xp": 780}},
          "Goblin": {"type": "Goblin", "minlevel": 10, "attack": "stabbed", "stats": {"health": 85, "damagemin": 12, "damagemax": 25, "coinsmin": 8, "coinsmax": 12, "xp": 450}},
          "Slime": {"type": "Slime", "minlevel": 5, "attack": "made you feel gross ", "stats": {"health": 120, "damagemin": 4, "damagemax": 6, "coinsmin": 3, "coinsmax": 4, "xp": 80}},
          "Rat": {"type": "Rat", "minlevel": 1, "attack": "bit", "stats": {"health": 50, "damagemin": 2, "damagemax": 5, "coinsmin": 1, "coinsmax": 2, "xp": 20}}}
