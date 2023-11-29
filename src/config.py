import json

# load bot token from json file
with open('bot.json') as file:
    botConfig = json.load(file)

with open('config.json') as file:
    config = json.load(file)