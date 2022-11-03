import discord
from keys import token
from player import Player
from enemy import Enemy
from save import Save
from story import storyline as sl


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

PLAYERS = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):

    if message.author == client.user:
        # if this is true the message came from the bot so we dont reply
        return

    if message.content.startswith("$start"):
        PLAYERS[message.author.name] = Player(message.author.name, message)
        await PLAYERS[message.author.name].hello()

    if message.content.startswith("$help"):
        await message.channel.send(sl["help"])

    if message.content.startswith("$stats"):
        await PLAYERS[message.author.name].showstats()

    if message.content.startswith("$gear"):
        await PLAYERS[message.author.name].showgear()

    if message.content.startswith("$levelup"):
        await PLAYERS[message.author.name].increasexp(int(message.content.split()[1]))

    if message.content.startswith("$save"):
        Save(PLAYERS)


client.run(token)
