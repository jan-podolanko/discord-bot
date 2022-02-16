import discord
from discord.ext import commands
from datetime import date, time, datetime

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #bot sends number of days since houseki no kuni hiatus :(
    @commands.command()
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        delta = date.today() - hiatus
        await ctx.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    @commands.command()
    async def time_now(self, ctx):
        today = datetime.now()
        date_time = today.strftime("%d/%m/%Y, %H:%M:%S")
        await ctx.send(date_time)
    
    @commands.command()
    async def reminder():
        return