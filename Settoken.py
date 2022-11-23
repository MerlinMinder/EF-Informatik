with open("Keys.py", "w") as keyfile:
    token = input("Enter your discord bot token here: ")
    keyfile.write(f"token = '{token}'")
    print("The token has been saved\nHave fun with the bot")
