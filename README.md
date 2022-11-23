# discordRPG

This application runs a Discord bot user. You can enter commands or react to messages in the discord server where the bot is running. It then takes you through a grindy RPG which takes a total of about 2 hours to complete. The main focus is put on fighting and leveling up your character. 

## How to use

### Creating a discord account

If you already have a discord account and server set up skip to: Implementing the bot

Otherwise create an account [here](https://support.discord.com/hc/en-us/articles/360033931551-Getting-Started)

Next create a new server [like this](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-)

### Implementing the bot

The main library used in this project is discord.py

They explain the process of implementing the bot really well: [check it out](https://discordpy.readthedocs.io/en/stable/discord.html)

### Downloading the code

Copy and paste this into the terminal

#### Windows
```
git clone https://github.com/MerlinMinder/discordRPG.git 
cd discordRPG
py -m pip install discord
```

#### Unix/macOS
```
git clone https://github.com/MerlinMinder/discordRPG.git 
cd discordRPG
python3 -m pip install discord
```

### Entering your token

run the code below and paste your token when the text appears

```
Settoken.py
```

### Running the bot

Enter this code to run the bot
To stop it press ctrl+c in the terminal

#### Windows
```
py Bot.py
```

#### Unix/macOS
```
python3 Bot.py
```
