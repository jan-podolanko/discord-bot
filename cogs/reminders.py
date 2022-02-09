import discord
from discord.ext import commands
from datetime import date
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from apscheduler.triggers.cron import CronTrigger
#trying to make sense of apscheduler, so far kind of a mess

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #async def reminder(self, ctx):
    #    await ctx.send("i remind :)")

    #today's date
    @commands.command()
    async def today(self, ctx):
        await ctx.send(date.today())

    #bot sends number of days since houseki no kuni hiatus :(
    @commands.command()
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        delta = date.today() - hiatus
        await ctx.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    #@bot.listen
    #async def on_ctx(ctx):
    #    if ctx.author == bot.user:
    #        if ctx == sad.jpg

    """  async def func(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(815254981736529941)
        await channel.send("i remind :)")

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.func, CronTrigger(hour = "17", minute="27", second="0"))
        scheduler.start() """
