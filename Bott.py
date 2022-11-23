import discord
import copy
from Keys import token
from Savee import getPlayers, savePlayers
from Lines import lines
from Playerr import Player
from Values import *

"""
The discord client requires intents to be set in order for it 
to be able to access certain options and data

message_content - can read the messages
reactions - can see the reactions to messages
members - can see the members of the server
"""
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True


class MyClient(discord.Client):
    """
    Client class which inherits from the discord client
    This enables overwriting and access to all discord client functions

    The main functions used are on_message, on_reaction_add, on_ready 
    they get called by the client whenever a certain event occurs
    in the server which is described in the name of the function

    __init__ takes the intents as an argument and calls super() from
    the discord.Client

    self.players saves all the players as a key value pair where
    the key is the name and the Player object is the value

    self.messages saves the most recent message from each player where
    the key is the name and the value is the message
    This is used to check if the player who interacts with a message 
    is doing that to the one intended for him
    """

    def __init__(self, *, intents: discord.Intents, **options: any) -> None:
        super().__init__(intents=intents, **options)
        self.players = {}
        self.messages = {}

    # All functions are async to enable multiple people
    # and messages to be handled at the same time
    async def on_message(self, message):
        """
        Check if messsage is a command:
        Commands start with a $

        General commands include $start, $clear, $save and $help
        they can be run by anyone

        Other commands are only run if the member has a Player() character
        """

        # Check if message was sent by bot and return if true
        if message.author == self.user:
            return

        elif message.content.startswith("$start"):
            # Create new Player() character and save it in self.players as mentioned above
            self.players[message.author] = Player(
                message.author.name, channel=message.channel)

            # Send hello message
            await self.players[message.author].hello()

            # Send class selection message
            self.messages[message.author] = await message.channel.send("Please choose a class:\n\nWarrior, Ranger, Mage")
            for emoji in classes.keys():
                await self.messages[message.author].add_reaction(emoji)

        elif message.content.startswith("$clear"):
            # Clears/deletes the last 100 messages in the channel
            await message.channel.purge()

        elif message.content.startswith("$save"):
            savePlayers(self.players)
            savemessage = await message.channel.send("Saved all players current stats and gear")
            await savemessage.delete(delay=3)

        elif message.content.startswith("$help"):
            # General help message that explains all commands
            return await message.channel.send(lines["help"])

        elif message.content.startswith("$"):
            # Check if member has created a Player() character with $start
            # If no character is present return help message
            if self.players.get(message.author) == None:
                return await message.channel.send(lines["help"])

            # Sets players channel to current channel where message was sent
            self.players[message.author].channel = message.channel

            # .delete(delay=X) deletes the message after X seconds (non-blocking)

            """Player specific commands"""

            if message.content.startswith("$stats"):
                statmessage = await self.players[message.author].showstats()
                await statmessage.delete(delay=10)

            if message.content.startswith("$gear"):
                gearmessage = await self.players[message.author].showgear()
                await gearmessage.delete(delay=10)

            if message.content.startswith("$combat"):
                # general message informing user of his options
                fightmessage = await message.channel.send(lines["combat"])

                # add enemys as reaction emojis
                for emoji in enemyemojis.keys():
                    # checks if the minimum level required to fight the enemy
                    # is smaller or equal to players level
                    if self.players[message.author].check_level(ENEMYS[enemyemojis[emoji]]['minlevel']):
                        await fightmessage.add_reaction(emoji)

                # Set combat message as recent message for user
                self.messages[message.author] = fightmessage

            if message.content.startswith("$shop"):
                # only display weapons specific to the chosen class
                shopweapons = SHOP[self.players[message.author].classtype]
                shoptext = f"**SHOP**\n\nCoins:  ***{self.players[message.author].stats['coins']}***\n\n"
                colorcount = 0

                # add weapon object to message text after formatting
                for key, element in shopweapons.items():
                    shoptext += f"{shopemojis[colorcount]}{element['type'].capitalize()}:  damage - *{element['damage']}*  durability - *{element['durability']}*   COST - **{element['cost']}**\n"
                    colorcount += 1
                shoptext += "\nPotions\n\n"

                # add potion object to message text after formatting
                for key, element in POTIONS.items():
                    # only display dragon potion after
                    # player has reached level 100
                    if key == "dragon":
                        if self.players[message.author].stats['level'] < 100:
                            continue
                    shoptext += f"{shopemojis[colorcount]}{element['type'].capitalize()}:  effect - *{element['effect']}*  COST - **{element['cost']}**\n"
                    colorcount += 1

                # Set shop message as recent message for user
                self.messages[message.author] = await message.channel.send(shoptext)

                # add weapons and potions as reaction emojis
                for emoji in shopemojis:
                    # check for dragon potion again
                    if emoji == "🏺":
                        if self.players[message.author].stats['level'] < 100:
                            continue

                    await self.messages[message.author].add_reaction(emoji)

                # add exit reaction emoji
                await self.messages[message.author].add_reaction("🚫")

            if message.content.startswith("$class"):
                # Sends message with your class and its attribute
                classmessage = await message.channel.send(f"Your class {self.players[message.author].classtype} has the attribute of\n\n{classes[str(self.players[message.author].classtype)]}")
                await classmessage.delete(delay=10)

            if message.content.startswith("$armory"):
                # armory unlocks after player level 60
                if self.players[message.author].check_level(60) == False:
                    failmessage = await message.channel.send("Reach level **60** to unlock this content")
                    await failmessage.delete(delay=3)
                    return

                armorytext = f"**ARMORY**\n\nCoins:  ***{self.players[message.author].stats['coins']}***\n\n"
                emojicount = 0

                # add armor object to message text after formatting
                for key, element in ARMOR.items():
                    armorytext += f"{list(armoryemojis.values())[emojicount]}{element['type'].capitalize()}:  Health  +*{element['health']}*   COST - **{element['cost']}**\n"
                    emojicount += 1

                # Set armory message as recent message for user
                self.messages[message.author] = await message.channel.send(armorytext)

                # add armor as reaction emojis
                for emoji in armoryemojis.values():
                    await self.messages[message.author].add_reaction(emoji)

                # add exit reaction
                await self.messages[message.author].add_reaction("🚫")

            # delete command message
            await message.delete()

    async def on_reaction_add(self, reaction, user):
        """
        Check if reaction is valid:
        Valid reactions are all emojis in Values.py

        Only the member which the message corresponds to 
        can add a reaction
        """

        # Check if reaction was added by bot and return if true
        if user == self.user:
            return

        # Check if the reacted message is the
        # recent message of the same member that reacted
        if reaction.message == self.messages[user]:

            # reactions corresponding to the class selection
            if reaction.emoji in classes.keys():
                await self.players[user].setclass(reaction.emoji)

                # remove class selection message from players recent message
                await self.messages[user].delete()

                classmessage = await reaction.message.channel.send(f"Your class {reaction.emoji} has the attribute of\n\n{classes[str(reaction.emoji)]}")
                await classmessage.delete(delay=5)

            # reaction corresponding to shop weapons
            elif reaction.emoji in shopemojis[:6]:
                # create copy of weapon object -> see Values.py for explanation
                weapon = copy.deepcopy(list(SHOP[self.players[user].classtype].values())[
                    shopemojis.index(reaction.emoji)])

                # check if player has enough coins for weapon cost
                if self.players[user].stats['coins'] >= weapon["cost"]:
                    # remove shop message from players recent messages
                    await self.messages[user].delete()
                    buyconfirm = await self.players[user].buyweapon(weapon)
                    await buyconfirm.delete(delay=4)
                else:
                    failmessage = await reaction.message.channel.send("Not enough coins available for this purchase")
                    await failmessage.delete(delay=2)
                    await reaction.remove(user)

            # reaction corresponding to shop potions
            elif reaction.emoji in shopemojis[6:]:
                # create copy of potion object -> see weapon
                potion = copy.deepcopy(
                    list(POTIONS.values())[shopemojis.index(reaction.emoji)-6])

                # check if player has to little coins for purchase
                if self.players[user].stats['coins'] < potion["cost"]:
                    failmessage = await reaction.message.channel.send("Not enough coins available for this purchase")
                    await failmessage.delete(delay=2)
                    await reaction.remove(user)

                # the player can have a maximum of ten potions
                elif len(self.players[user].equipment['potions']) >= 10:
                    failmessage = await reaction.message.channel.send("You can't have more then 10 potions\nUse them up in combat!")
                    await failmessage.delete(delay=3)
                    await reaction.remove(user)
                else:
                    await self.messages[user].delete()
                    buyconfirm = await self.players[user].buypotion(potion)
                    await buyconfirm.delete(delay=4)

            # reaction corresponding to armory armor
            elif reaction.emoji in armoryemojis.values():
                # create copy of armor object -> see weapon
                armor = copy.deepcopy(ARMOR[reaction.emoji])

                # check if player has to little coins for purchase
                if self.players[user].stats['coins'] < armor["cost"]:
                    failmessage = await reaction.message.channel.send("Not enough coins available for this purchase")
                    await failmessage.delete(delay=2)
                    await reaction.remove(user)

                # check if player has already bought this armor
                elif self.players[user].gear[armor['type']]:
                    failmessage = await reaction.message.channel.send("You already have this piece of armor\nCheck it out with $gear!")
                    await failmessage.delete(delay=3)
                    await reaction.remove(user)
                else:
                    await self.messages[user].delete()
                    buyconfirm = await self.players[user].buyarmor(armor)
                    await buyconfirm.delete(delay=4)

            # reaction corresponding to combat enemy
            elif reaction.emoji in enemyemojis.keys():
                # create copy of enemy object -> see weapon
                enemy = copy.deepcopy(ENEMYS[enemyemojis[reaction.emoji]])

                await reaction.message.delete()

                # initialize fight sequence
                self.messages[user] = await self.players[user].fight(enemy)

            # attack
            elif reaction.emoji == "⚔️":
                await reaction.message.delete()
                # list comprehension to find highest
                # enemy player is able to fight
                maxenemy = [enemy for enemy in ENEMYS.values(
                ) if enemy['minlevel'] <= self.players[user].stats['level']][0]['type']

                # start attack -> leads to three results
                self.messages[user] = await self.players[user].attack(maxenemy)

                # 1. if player killed enemy it is set to None
                if self.players[user].enemy == None:
                    # give rewards to player
                    statsmessage = await self.players[user].levelup()
                    await self.messages[user].delete(delay=5)
                    await statsmessage.delete(delay=5)

                # 2. check if player died -> helath <= 0
                elif self.players[user].stats["health"] <= 0:
                    # kill player
                    deathmessage = await self.players[user].kill()
                    await self.messages[user].delete(delay=5)
                    await deathmessage.delete(delay=15)

                # 3. else continue with fighting
                else:
                    await self.messages[user].delete(delay=5)
                    self.messages[user] = await self.players[user].fight()

            # heal
            elif reaction.emoji == "❤️‍🩹":
                # check if player has potions available
                if self.players[user].equipment['potions']:
                    await self.messages[user].delete()
                    self.messages[user] = await self.players[user].showpotions()
                else:
                    await reaction.message.edit(content="**You have no healing potions available!**\n\nBuy more in the shop before your next battle")
                    await reaction.message.delete(delay=4)
                    self.messages[user] = await self.players[user].fight()

            # retreat/escape
            elif reaction.emoji == "🆘":
                await reaction.message.delete()
                escapemessage = await self.players[user].escape()
                await escapemessage.delete(delay=5)

            # reaction corresponding to heal potion
            elif reaction.emoji in healemojis:
                await self.messages[user].delete()

                # heals player for potion effect
                # potion position corresponding to position of reaction emoji
                healmessage = await self.players[user].heal(healemojis.index(reaction.emoji))

                # continue with fight
                self.messages[user] = await self.players[user].fight()
                await healmessage.delete(delay=3)

            # exit heal menu
            elif reaction.emoji == "❌":
                """exits heal menu and returns to fight"""
                await self.messages[user].delete()
                self.messages[user] = await self.players[user].fight()

            # quit/exit
            elif reaction.emoji == "🚫":
                """exits shop or armory"""
                await self.messages[user].delete()

            # reaction is not part of any valid reactions
            else:
                await reaction.remove(user)

        # reaction is from another user
        else:
            await reaction.remove(user)

    # runs when bot is first started
    async def on_ready(self):
        # set botname to RPG MARSTER
        await self.user.edit(username="RPG MASTER")
        print(f"Bot is online as {self.user}")

        # Get all members of server and load existing
        # Player() characters for each member
        members = []
        for member in self.get_all_members():
            members.append(member)
        self.players = getPlayers(
            members)


if __name__ == "__main__":
    # create client and run with discord server token
    client = MyClient(intents=intents)
    client.run(token)
