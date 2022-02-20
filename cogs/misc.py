from discord.ext import commands
import discord

class Miscellaneous(commands.Cog):
    #bot responds to greetings :)
    @commands.command()
    async def hello(self, message, test):
        await message.send(f'Hello! {test}')

    #command to shut bot down (+ gif to accompany that)
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down bot.")
        await ctx.send(file=discord.File('./pics/disappear-peace-out.gif'))
        exit()