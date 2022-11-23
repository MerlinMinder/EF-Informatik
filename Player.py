import random
from Lines import lines
from Enemy import Enemy
from Values import *


class Player(object):
    """
    Player gets created by Client and stores essential data
    """

    # when loading existing data all kwargs are set to loaded data
    # otherwise the default value is used
    def __init__(self, name, channel=None, stats={"health": 100, "maxhealth": 100, "damage": 10,
                                                  "level": 1, "xp": 0, "coins": 10}, equipment={"weapon": None, "potions": [], }, gear={"helmet": None, "chestplate": None,
                                                                                                                                        "leggins": None, "boots": None}, attacktype="hit", classtype="🗡️") -> None:
        """
        self.channel is the current channel where the player is writing
        it needs to be save so the bot wirtes its messages in the same channel

        The other variables are all stats and values used for the game
        """
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

    # send welcome message explaining the game
    async def hello(self):
        return await self.channel.send(lines["hello"] + self.name)

    # turns stats object into formatted string and sends it
    async def showstats(self):
        stattext = ""
        # loop over all stats (health, damage, ...)
        for key, value in self.stats.items():
            stattext += f"{key.capitalize()} - {value}\n"

        # return sent message to be able to delete it later
        return await self.channel.send("_\nYour new stats are:\n" + stattext + "\n_")

    # turns gear and equipment object into formatted string and sends it
    async def showgear(self):
        # loop over all potions and list them up
        potioncontent = ""
        for i, potion in enumerate(self.equipment['potions']):
            potioncontent += f"{i+1}. {potion['type']} {potion['effect']}\n"
         # do the same for all armor
        armorcontent = ""
        for key, armor in self.gear.items():
            # check if ther is no armor and add a different string
            if armor == None:
                armorcontent += f"{key.capitalize()}: None\n"
            else:
                armorcontent += f"{armoryemojis[key]} {key.capitalize()}:  +{armor['health']} Health\n"

        # return sent message to be able to delete it later
        return await self.channel.send("_\nYour current gear is:\n\n" + f"Weapon - {self.equipment['weapon']}\n\n" + f"Potions - \n{potioncontent}\n" + f"Armor - \n{armorcontent}")

    # return if playerlevel is enough for minlevel
    def check_level(self, minlevel):
        return self.stats["level"] >= minlevel

    # sets the class type and change
    # object variables depending on class
    async def setclass(self, classtype):
        self.classtype = classtype
        if self.classtype == "🧙‍♂️":
            self.stats['damage'] = 6
        if self.classtype == "🏹":
            self.evasion += 2

    # adds the extra xp that has been given on enemy defeat
    # to existing xp and checks for levelup automatically
    async def levelup(self):
        if self.extraxp != 0:
            self.stats["xp"] += self.extraxp
            self.extraxp = 0
            return await self._checklevelup()

    # gets called by levelup()
    async def _checklevelup(self):

        # checks if xp is higher than the one necessary to level up
        # to level up the needed xp is equal to the level times 10
        # -> to level up to level 12 it takes 120 xp
        while self.stats["xp"] >= self.stats["level"] * 10:
            # remove xp needed to level up
            self.stats["xp"] -= self.stats["level"] * 10

            # add to stats
            self.stats["level"] += 1
            self.stats["health"] += 10
            self.stats["maxhealth"] += 10
            self.stats["coins"] += 10

            # mage gets less damage
            if self.classtype == "🧙‍♂️":
                self.stats["damage"] += 1.6
            else:
                self.stats["damage"] += 2

            # sends "You leveled up"
            await self.channel.send(lines["levelup"])

            # send special message on level 60 and 100
            if self.stats["level"] == 60:
                await self.channel.send("!!NICE!!\n\nYou reached level 60 and unlocked the *armory*\n\nCheck it out with **$armory** to get guud")

            if self.stats["level"] == 100:
                await self.channel.send("!!WOW!!\n\nYou reached level **100** and unlocked the *BOSS*\n\nCheck in the **$shop** for a new item to help you out")

        # calls showstats to display the new stats that have been added
        return await self.showstats()

    # gets called when the player health is <= 0
    async def kill(self):
        # replenishes health to max
        self.stats["health"] = self.stats["maxhealth"]

        # take away half the coins
        self.stats['coins'] = int(self.stats['coins']/2)

        # delete all items and gear, remove enemy
        self.equipment = {"weapon": None, "potions": [], }
        self.gear = {"helmet": None, "chestplate": None,
                     "leggins": None, "boots": None}
        self.enemy = None

        # return sent message to be able to delete it later
        return await self.channel.send(f"You were **killed** and lost ALL your items and *half* your coins!\nType $stats and $gear to view your new stats")

    # removes coins equal to cost and adds item to player
    async def buyweapon(self, weapon):
        self.stats['coins'] -= weapon["cost"]

        # replaces existing weapon with new one
        self.equipment["weapon"] = weapon
        return await self.channel.send(f"You just bought a **{weapon['type'].upper()}** for {weapon['cost']} coins\nType: $gear to see it")

    # removes coins equal to cost and adds item to player
    async def buypotion(self, potion):
        self.stats['coins'] -= potion["cost"]

        # adds potion to potion list (max 10)
        self.equipment['potions'].append(potion)
        return await self.channel.send(f"You just bought a **{potion['type'].upper()} potion** for {potion['cost']} coins\nType: $gear to see it")

    # removes coins equal to cost and adds item to player
    async def buyarmor(self, armor):
        self.stats['coins'] -= armor["cost"]

        # adds armor
        self.gear[armor['type']] = armor

        # increases stats according to armor description
        self.stats['maxhealth'] += armor['health']
        self.stats['health'] += armor['health']
        return await self.channel.send(f"You just bought a **{armor['type'].upper()}** for {armor['cost']} coins\nType: $gear to see it")

    # gets called when player has entered combat
    async def fight(self, enemystats=None):

        # check if new enemy has been added
        # if new enemy create it with the given stats
        if enemystats:
            self.enemy = Enemy(enemystats)

        # calculates damage from playerdamage + weapondamage
        damage = self.stats['damage']
        if self.equipment['weapon']:
            damage += self.equipment['weapon']['damage']

        # displays enemy health, player health and calculated damage
        message = await self.channel.send(f"_\nYou are fighting a {self.enemy.type} with {self.enemy.stats['health']} health\n\n" + f"You have {self.stats['health']} health and deal {int(damage)} damage\n\n" + lines["fight"])

        # add fight options as fightemojis
        for emoji in fightemojis.keys():
            await message.add_reaction(emoji)
        return message

    # gets called when player choose to attack the enemy
    async def attack(self, maxenemy):
        secondmessage = ""
        enemytype = self.enemy.type
        playerdamage = self.stats['damage']

        # when player has a weapon it increases
        # the damage by the weapondamage and
        # takes away 1 durability of the weapon
        if self.equipment['weapon']:
            self.attacktype = self.equipment['weapon']['attack']
            playerdamage += self.equipment['weapon']['damage']
            self.equipment['weapon']['durability'] -= 1

            # when the weapon has 0 durability it is destroyed/removed
            if self.equipment['weapon']['durability'] == 0:
                self.equipment['weapon'] = None
        else:
            self.attacktype = "hit"

        # in case of mage class the damage has a
        # 40% change of being multiplied by 1.75
        if self.classtype == "🧙‍♂️":

            # random number including 1, 10
            # if lower than 5 chance is 40%
            if random.randint(1, 10) < 5:
                playerdamage = playerdamage * 1.75

        # in case of ranger class the damage has a
        # 20% chace of being 0 (miss)
        if self.classtype == "🏹":

            # same as mage
            if random.randint(1, 10) < 3:
                playerdamage = 0

        # calls enemys attack function with calculated damage
        # enemy returns fight or dead
        if self.enemy.attack(int(playerdamage)) == "dead":

            # the enemys health is <= 0 which means you killed it
            # adds coins and xp according to enemy
            coins = random.randint(
                self.enemy.stats['coinsmin'], self.enemy.stats['coinsmax'])
            self.stats['coins'] += coins
            incxp = self.enemy.stats["xp"]

            # when enemy is not the highest enemy available to attack
            # the xp is cut by 90% giving only 1/10
            if self.enemy.type != maxenemy:
                incxp = int(incxp*0.1)
            self.extraxp += incxp

            # add kill message and remove enemy
            secondmessage = f"_\nYou killed the {self.enemy.type} and recieved {coins} coins and {incxp} xp"
            self.enemy = None

        else:

            # the enemys health is > 0 so
            # it gets a chance to damage the player
            damage = random.randint(
                self.enemy.stats['damagemin'], self.enemy.stats['damagemax'])

            # check if player evaded the attack
            # same as with archer damage check (miss)
            if random.randint(1, 10) < self.evasion:
                damage = 0

            # remove plaayerhealth according to damage dealt by enemy
            self.stats['health'] -= damage

            # add damage message
            secondmessage = f"It {self.enemy.attacktype} you for {damage} damage"

        # returns attack message and either damage or kill message
        return await self.channel.send(f"_\nYou {self.attacktype} the {enemytype} for {int(playerdamage)} damage\n\n" + secondmessage)

    # turns potion list into formatted string and returns it
    async def showpotions(self):
        potioncontent = ""
        # loop over potions and add them
        # to formatted string with corresponding index
        for i, potion in enumerate(self.equipment['potions']):
            potioncontent += f"{i+1}. {potion['type']} {potion['effect']}\n"

        # sends formatted potion list
        message = await self.channel.send(f"_\nHealth: {self.stats['health']},  Maxhealth: {self.stats['maxhealth']}\n\nYour available potions are currently:\n\n" + potioncontent)

        # add potion indexes as healemojis
        for index, element in enumerate(self.equipment['potions']):
            await message.add_reaction(healemojis[index])

        # add exit heal menu emoji
        await message.add_reaction("❌")
        return message

    # takes index of wanted potion, updates the stats (heal),
    # removes the potion and lets the enemy attack
    async def heal(self, index):

        # gets potion according to given index of potionlist
        potion = self.equipment['potions'][index]['type']
        inchealth = 0
        evasionflag = False

        # check potion type and add health accordingly
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
                # automatically sets helth to maxhealth
                inchealth = self.stats['maxhealth']

                # adds evasion chance for later attack
                self.evasion += 2
                evasionflag = True

        # check if new health is higher than maximum available health
        # if higher removes extra (illegal) health to match maxhealth
        if self.stats['health'] + inchealth > self.stats['maxhealth']:
            inchealth = self.stats['maxhealth'] - self.stats['health']
        self.stats['health'] += inchealth

        # delete potion from potionlist
        del self.equipment['potions'][index]

        # enemy gets to attack
        damage = random.randint(
            self.enemy.stats['damagemin'], self.enemy.stats['damagemax'])

        # check if player evaded the attack -> see attack
        if random.randint(1, 10) < self.evasion:
            damage = 0

        # same as attack
        self.stats['health'] -= damage
        secondmessage = f"It {self.enemy.attacktype} you for {damage} damage"

        # if dragon potion was used evaison was increased
        # remove extra evasion
        if evasionflag:
            self.evasion -= 2

        # retun heal message and damage message from enemy
        return await self.channel.send(f"_\nYou healed yourself for **{inchealth}** health\n\n" + secondmessage)

    # gets called when the player escapes a fight
    async def escape(self):

        # delete enemy and return escame message
        escapeenemy = self.enemy.type
        self.enemy = None
        return await self.channel.send(f"_\nYou escaped the {escapeenemy} with {self.stats['health']} health!\n\nBe better prepared next time\nCheck out the shop: **$shop**")
