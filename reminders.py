import discord
from discord.ext import commands
from datetime import date

class Reminders(commands.Cog):

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

    @commands.command()
    async def remind(self, ctx, arg, time):
        return