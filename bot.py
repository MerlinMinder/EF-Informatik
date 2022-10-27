import discord
from keys import token

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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

    if message.content.startswith("$multiply"):
        await message.channel.send(int(message.content.split()[1])*int(message.content.split()[2]))


client.run(token)
