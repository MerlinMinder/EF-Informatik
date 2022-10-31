import discord
from keys import token
from player import Player
from enemy import Enemy


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

    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello, {message.author.name}')

    if message.content.startswith("$start"):
        PLAYERS[message.author.name] = Player(message.author.name, message)
        await PLAYERS[message.author.name].hello()

    if message.content.startswith("$levelup"):
        await PLAYERS[message.author.name].levelup(int(message.content.split()[1]))

    if message.content.startswith("$multiply"):
        numbers = message.content.split()[1]
        await message.channel.send(int(numbers.split("*")[0])*int(numbers.split("*")[1]))

    if message.content.startswith("$calculate"):
        calculate = message.content.split()[1]
        if calculate[1] == "-":
            await message.channel.send(int(calculate[0])-int(calculate[2]))

        if calculate[1] == "+":
            await message.channel.send(int(calculate[0])+int(calculate[2]))

        if calculate[1] == "/":
            await message.channel.send(int(calculate[0])/int(calculate[2]))

        if calculate[1] == "*":
            await message.channel.send(int(calculate[0])*int(calculate[2]))


client.run(token)
