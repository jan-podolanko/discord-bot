from posixpath import split
import discord
from discord.ext import commands
from datetime import date, time, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
        self.scheduler.start()

    #sends number of days since houseki no kuni hiatus :(
    @commands.command()
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        delta = date.today() - hiatus
        await ctx.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    #function neccessary to send reminder messages
    async def rem(self,context,message):
        await context.send(f'Reminder: "{message}"')

    #sets up periodic reminders
    @commands.command()
    async def remind(self, ctx, msg, time, week_day=None, day_of_month=None):
        h,m = time.split(':')
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=f"{msg} on {time}", day=day_of_month, day_of_week=week_day, hour=int(h), minute=int(m))

    #sets up a single reminder at specific date
    @commands.command()
    async def remind_once(self, ctx, msg, time, date):
        h,m = [int(i) for i in time.split(':')]
        da,mo,ye = [int(i) for i in date.split('.')]
        self.scheduler.add_job(self.rem,'date', args=[ctx,msg], name=f"{msg} on {date}, {time}", run_date=datetime(ye,mo,da,h,m,0))

    #sends list of reminders
    @commands.command()
    async def list(self,ctx):
        await ctx.send(self.scheduler.get_jobs())
    
    #removes reminders by id
    @commands.command()
    async def remove(self,ctx,id):
        self.scheduler.remove_job(id)
        ctx.send(f"Succesfully removed reminder with id {id}")