import json

# load bot token from json file
with open('bot.json') as file:
    botConfig = json.load(file)