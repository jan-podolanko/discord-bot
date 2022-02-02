from discord.ext import commands
import logging
import random
import requests
from datetime import date
from discord import File
import json

#logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!')

emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']

#message on logging on
@bot.event
async def on_ready():
    channel = bot.get_channel(815254981736529941)
    await channel.send('I have been awakened!')

#reacting with random emojis to every message
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    await message.add_reaction(emojis[random.randrange(len(emojis))])

#bot responds to greetings :)
@bot.command()
async def hello(message):
    await message.send('Hello!')

#bot messages with random kanye quote from api
@bot.command()
async def kanye(message):
    quote = requests.get('https://api.kanye.rest/')
    json_quote = quote.json()
    await message.send('"{}" - Kanye West'.format(json_quote.get("quote")))

#today's date
@bot.command()
async def today(message):
    await message.send(date.today())

#bot sends number of days since houseki no kuni hiatus :(
@bot.command()
async def hiatus(message):
    hiatus = date(2020,12,25)
    delta = date.today() - hiatus
    await message.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
    await message.send(file=File('./pics/sad.jpg'))

#@bot.listen
#async def on_message(message):
#    if message.author == bot.user:
#        if message == sad.jpg

#@bot.command()
#async def quote(message):
#    await message.send("test")
with open("token.json","r") as token:
    data = json.load(token)
    bot.run(data.get("token"))
