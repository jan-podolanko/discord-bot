from discord.ext import commands
import random, discord, json

class Events(commands.Cog):
    def __init__(self, bot):
        self.emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '🥲', '☺️', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🥸', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        self.bot = bot

    #simple error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        else:
            message = str(error)
        await ctx.send(message, delete_after=15)

    #message on logging on (and enabling discord together)
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(815254981736529941)
        await channel.send('I have been awakened!', delete_after=15)
        with open("token.json","r") as token:
            data = json.load(token)

    #if any message contains one of the defined words, bot responds appropriately
    #(as well as reacting with random emojis to some messages)
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "turbo" in ctx.content.lower():
            await ctx.reply(file=discord.File('./pics/so-true.gif'))
        if "jan" in ctx.content.lower():
            await ctx.add_reaction("🇯")
            await ctx.add_reaction("🇦")
            await ctx.add_reaction("🇳")
        roll = random.randrange(15)
        if roll == 1 and ctx.author != self.bot.user:
            await ctx.add_reaction(self.emojis[random.randrange(len(self.emojis))])