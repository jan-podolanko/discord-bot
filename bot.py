import discord, logging, json
from discord.ext import commands
from cogs.misc import Miscellaneous
from cogs.quotes import Quotes
from cogs.reminders import Reminders
from cogs.events import Events
from discord_together import DiscordTogether

#logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#activity set in the constructor, apparently the bot breaks if set in on_ready() event
activity = discord.Activity(type=discord.ActivityType.listening, name="just vibing")
desc = "WeebReminder is a bot that does stuff."
bot = commands.Bot(command_prefix='!', description=desc, activity=activity, status=discord.Status.idle)

#adding neccessary cogs
bot.add_cog(Quotes())
bot.add_cog(Reminders(bot))
bot.add_cog(Miscellaneous())
bot.add_cog(Events(bot))

#running the bot with hidden token
with open("token.json","r") as token:
    data = json.load(token)
    bot.run(data.get("token"))