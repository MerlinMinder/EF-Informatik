class Enemy:

    def __init__(self, init) -> None:
        self.stats = init["stats"]
        self.type = init["type"]
        self.attacktype = init["attack"]

    def attack(self, damage):
        self.stats["health"] -= damage
        if self.stats["health"] < 1:
            return "dead"
        return "fight"
