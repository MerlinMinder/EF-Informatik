class Player(object):
    def __init__(self, user, message) -> None:
        self.level = 0
        self.name = user
        self.stats = {"health": 100, "damage": 10}
        self.channel = message.channel

    async def hello(self):
        await self.channel.send(f"Hello {self.name}")

    async def levelup(self, increase):
        self.level += increase
        await self.channel.send(f"Your level is {self.level}")
