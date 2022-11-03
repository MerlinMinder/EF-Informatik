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
