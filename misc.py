from discord.ext import commands
import requests

class Miscellaneous(commands.Cog):
    #bot responds to greetings :)
    @commands.command()
    async def hello(self, message, test):
        await message.send(f'Hello! {test}')
