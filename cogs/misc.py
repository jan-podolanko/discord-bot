from discord.ext import commands
import discord

class Miscellaneous(commands.Cog):
    #bot responds to greetings :)
    @commands.command()
    async def hello(self, ctx, test):
        await ctx.send(f'Hello! {test}')

    #command to shut bot down (+ gif to accompany that)
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down bot.")
        await ctx.send(file=discord.File('./pics/disappear-peace-out.gif'))
        exit()

    @commands.command()
    async def slide(self, ctx):
        await ctx.author.send("👀")