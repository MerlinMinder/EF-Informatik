import random
from Lines import lines
from Enemy import Enemy
from Values import *


class Player(object):

    def __init__(self, name, channel=None, stats={"health": 100, "maxhealth": 100, "damage": 10,
                                                  "level": 1, "xp": 0, "coins": 10}, equipment={"weapon": None, "potions": [], }, gear={"helmet": None, "chestplate": None,
                                                                                                                                        "leggins": None, "boots": None}, attacktype="hit", classtype="🗡️") -> None:
        self.channel = channel
        self.name = name
        self.stats = stats
        self.equipment = equipment
        self.gear = gear
        self.attacktype = attacktype
        self.extraxp = 0
        self.enemy = None
        self.classtype = classtype
        self.evasion = 1

    async def hello(self):
        return await self.channel.send(lines["hello"] + self.name)

    async def showstats(self):
        stattext = ""
        for key, value in self.stats.items():
            stattext += f"{key.capitalize()} - {value}\n"
        return await self.channel.send("_\nYour new stats are:\n" + stattext + "\n_")

    async def showgear(self):
        potioncontent = ""
        for i, potion in enumerate(self.equipment['potions']):
            potioncontent += f"{i+1}. {potion['type']} {potion['effect']}\n"
        armorcontent = ""
        for key, armor in self.gear.items():
            if armor == None:
                armorcontent += f"{key.capitalize()}: None\n"
            else:
                armorcontent += f"{armoryemojis[key]} {key.capitalize()}:  +{armor['health']} Health\n"
        return await self.channel.send("_\nYour current gear is:\n\n" + f"Weapon - {self.equipment['weapon']}\n\n" + f"Potions - \n{potioncontent}\n" + f"Armor - \n{armorcontent}")

    def check_level(self, minlevel):
        return self.stats["level"] >= minlevel

    async def setclass(self, classtype):
        self.classtype = classtype
        if self.classtype == "🧙‍♂️":
            self.stats['damage'] = 6
        if self.classtype == "🏹":
            self.evasion += 2

    async def levelup(self):
        if self.extraxp != 0:
            self.stats["xp"] += self.extraxp
            self.extraxp = 0
            return await self._checklevelup()

    async def _checklevelup(self):
        while self.stats["xp"] >= self.stats["level"] * 10:
            self.stats["xp"] -= self.stats["level"] * 10
            self.stats["level"] += 1
            self.stats["health"] += 10
            self.stats["maxhealth"] += 10
            if self.classtype == "🧙‍♂️":
                self.stats["damage"] += 1.6
            else:
                self.stats["damage"] += 2
            self.stats["coins"] += 10
            await self.channel.send(lines["levelup"])
            if self.stats["level"] == 60:
                await self.channel.send("!!NICE!!\n\nYou reached level 60 and unlocked the *armory*\n\nCheck it out with **$armory** to get guud")

            if self.stats["level"] == 100:
                await self.channel.send("!!WOW!!\n\nYou reached level **100** and unlocked the *BOSS*\n\nCheck in the **$shop** for a new item to help you out")
        return await self.showstats()

    async def kill(self):
        self.stats["health"] = self.stats["maxhealth"]
        self.stats['coins'] = int(self.stats['coins']/2)
        self.equipment = {"weapon": None, "potions": [], }
        self.gear = {"helmet": None, "chestplate": None,
                     "leggins": None, "boots": None}
        self.enemy = None
        return await self.channel.send(f"You were **killed** and lost ALL your items and *half* your coins!\nType $stats and $gear to view your new stats")

    async def buyweapon(self, weapon):
        self.stats['coins'] -= weapon["cost"]
        self.equipment["weapon"] = weapon
        return await self.channel.send(f"You just bought a **{weapon['type'].upper()}** for {weapon['cost']} coins\nType: $gear to see it")

    async def buypotion(self, potion):
        self.stats['coins'] -= potion["cost"]
        self.equipment['potions'].append(potion)
        return await self.channel.send(f"You just bought a **{potion['type'].upper()} potion** for {potion['cost']} coins\nType: $gear to see it")

    async def buyarmor(self, armor):
        self.stats['coins'] -= armor["cost"]
        self.gear[armor['type']] = armor
        self.stats['maxhealth'] += armor['health']
        self.stats['health'] += armor['health']
        return await self.channel.send(f"You just bought a **{armor['type'].upper()}** for {armor['cost']} coins\nType: $gear to see it")

    async def fight(self, enemystats=None):
        if enemystats:
            self.enemy = Enemy(enemystats)
        damage = self.stats['damage']
        if self.equipment['weapon']:
            damage += self.equipment['weapon']['damage']
        message = await self.channel.send(f"_\nYou are fighting a {self.enemy.type} with {self.enemy.stats['health']} health\n\n" + f"You have {self.stats['health']} health and deal {int(damage)} damage\n\n" + lines["fight"])
        for emoji in fightemojis.keys():
            await message.add_reaction(emoji)
        return message

    async def attack(self, maxenemy):
        secondmessage = ""
        enemytype = self.enemy.type
        playerdamage = self.stats['damage']
        if self.equipment['weapon']:
            self.attacktype = self.equipment['weapon']['attack']
            playerdamage += self.equipment['weapon']['damage']
            self.equipment['weapon']['durability'] -= 1
            if self.equipment['weapon']['durability'] == 0:
                self.equipment['weapon'] = None
        else:
            self.attacktype = "hit"
        if self.classtype == "🧙‍♂️":
            if random.randint(1, 10) < 4:
                playerdamage = playerdamage * 1.75
        if self.classtype == "🏹":
            if random.randint(1, 10) < 3:
                playerdamage = 0
        if self.enemy.attack(int(playerdamage)) == "dead":
            coins = random.randint(
                self.enemy.stats['coinsmin'], self.enemy.stats['coinsmax'])
            self.stats['coins'] += coins
            incxp = self.enemy.stats["xp"]
            if self.enemy.type != maxenemy:
                incxp = int(incxp*0.1)
            self.extraxp += incxp
            secondmessage = f"_\nYou killed the {self.enemy.type} and recieved {coins} coins and {incxp} xp"
            self.enemy = None
        else:
            damage = random.randint(
                self.enemy.stats['damagemin'], self.enemy.stats['damagemax'])

            if random.randint(1, 10) < self.evasion:
                damage = 0
            self.stats['health'] -= damage
            secondmessage = f"It {self.enemy.attacktype} you for {damage} damage"
        return await self.channel.send(f"_\nYou {self.attacktype} the {enemytype} for {int(playerdamage)} damage\n\n" + secondmessage)

    async def showpotions(self):
        potioncontent = ""
        for i, potion in enumerate(self.equipment['potions']):
            potioncontent += f"{i+1}. {potion['type']} {potion['effect']}\n"
        message = await self.channel.send(f"_\nHealth: {self.stats['health']},  Maxhealth: {self.stats['maxhealth']}\n\nYour available potions are currently:\n\n" + potioncontent)
        for index, element in enumerate(self.equipment['potions']):
            await message.add_reaction(healemojis[index])
        await message.add_reaction("❌")
        return message

    async def heal(self, index):
        potion = self.equipment['potions'][index]['type']
        inchealth = 0
        evasionflag = False
        match potion:
            case "tiny":
                inchealth = 50
            case "small":
                inchealth = int(self.stats['maxhealth'] * 0.25)
            case "medium":
                inchealth = int(self.stats['maxhealth'] * 0.50)
            case "large":
                inchealth = int(self.stats['maxhealth'] * 0.75)
            case "dragon":
                inchealth = self.stats['maxhealth']
                self.evasion += 2
                evasionflag = True
        if self.stats['health'] + inchealth > self.stats['maxhealth']:
            inchealth = self.stats['maxhealth'] - self.stats['health']
        self.stats['health'] += inchealth
        del self.equipment['potions'][index]
        damage = random.randint(
            self.enemy.stats['damagemin'], self.enemy.stats['damagemax'])

        if random.randint(1, 10) < self.evasion:
            damage = 0
        self.stats['health'] -= damage
        secondmessage = f"It {self.enemy.attacktype} you for {damage} damage"
        if evasionflag:
            self.evasion -= 2
        return await self.channel.send(f"_\nYou healed yourself for **{inchealth}** health\n\n" + secondmessage)

    async def escape(self):
        escapeenemy = self.enemy.type
        self.enemy = None
        return await self.channel.send(f"_\nYou escaped the {escapeenemy} with {self.stats['health']} health!\n\nBe better prepared next time\nCheck out the shop: **$shop**")
