from story import storyline as sl


class Player(object):

    def __init__(self, user, message) -> None:
        self.name = user
        self.stats = {"health": 100, "damage": 10,
                      "level": 1, "xp": 0, "coins": 10}
        self.gear = {"weapon": None, "helmet": None,
                     "chestplate": None, "leggins": None, "boots": None}
        self.channel = message.channel

    async def hello(self):
        await self.channel.send(sl["join"] + sl["help"])

    async def showstats(self):
        await self.channel.send(sl["stats"] + str(self.stats))

    async def showgear(self):
        await self.channel.send(sl["gear"] + str(self.gear))

    async def increasexp(self, xp):
        self.stats["xp"] += xp
        await self._checklevelup()

    async def _checklevelup(self):
        while self.stats["xp"] >= self.stats["level"] * 10:
            self.stats["xp"] -= self.stats["level"] * 10
            self.stats["level"] += 1
            self.stats["health"] += 10
            self.stats["damage"] += 2
            self.stats["coins"] += 10
            await self.channel.send(sl["levelup"])
        await self.showstats()

    async def fight(self):
        return await self.channel.send(sl["fight"])
