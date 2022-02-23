import discord
from discord.ext import commands
from datetime import date, time, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functools import partial

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
        self.scheduler.start()

    #bot sends number of days since houseki no kuni hiatus :(
    @commands.command()
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        delta = date.today() - hiatus
        await ctx.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    #bot gives current date and time
    @commands.command()
    async def time_now(self, ctx):
        today = datetime.now()
        date_time = today.strftime("%d/%m/%Y, %H:%M:%S")
        await ctx.send(date_time)

    async def rem(self,context,message):
        await context.send(f'Reminder: "{message}"')

    @commands.command()
    async def remind(self, ctx, msg, time, week_day=None, day_of_month=None):
        h,m = time.split(':')
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], day=day_of_month, day_of_week=week_day, hour=int(h), minute=int(m))