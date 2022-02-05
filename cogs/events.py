from discord.ext import commands
import random, discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        self.bot = bot
    #reacting with random emojis to every message
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        roll = random.randrange(15)
        if roll == 1:
            await ctx.add_reaction(self.emojis[random.randrange(len(self.emojis))])

    #error handling (found on tutorial)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "Something unexpected went wrong."
        await ctx.send(message)
        #await ctx.message.delete(delay=5)

    #message on logging on
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(815254981736529941)
        await channel.send('I have been awakened!')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "jan" in ctx.content.lower():
            await ctx.add_reaction("🇯")
            await ctx.add_reaction("🇦")
            await ctx.add_reaction("🇳")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "turbo" in ctx.content.lower():
            await ctx.reply(file=discord.File('./pics/so-true.gif'))