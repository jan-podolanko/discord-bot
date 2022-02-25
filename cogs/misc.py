from discord.ext import commands
import discord

class Miscellaneous(commands.Cog):
    #bot responds to greetings :)
    @commands.command(help="Bot says hello.")
    async def hello(self, ctx):
        await ctx.send(f'Hello! {ctx.author}')

    #command to shut bot down (+ gif to accompany that)
    @commands.command(help="Shuts bot down. Only available to bot owner.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down bot.")
        await ctx.send(file=discord.File('./pics/disappear-peace-out.gif'))
        exit()

    @commands.command(help="Slides into your dms.")
    async def slide(self, ctx):
        await ctx.author.send("👀")