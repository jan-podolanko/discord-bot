from discord.ext import commands
import random, discord, json
from discord_together import DiscordTogether

class Events(commands.Cog):
    def __init__(self, bot):
        self.emojis = ['๐', '๐', '๐', '๐', '๐', '๐', '๐', '๐คฃ', '๐ฅฒ', 'โบ๏ธ', '๐', '๐', '๐', '๐', '๐', '๐', '๐', '๐ฅฐ', '๐', '๐', '๐', '๐', '๐', '๐', '๐', '๐', '๐คช', '๐คจ', '๐ง', '๐ค', '๐', '๐ฅธ', '๐คฉ', '๐ฅณ', '๐', '๐', '๐', '๐', '๐', '๐', '๐', 'โน๏ธ', '๐ฃ', '๐', '๐ซ', '๐ฉ', '๐ฅบ', '๐ข', '๐ญ', '๐ค', '๐ ', '๐ก', '๐คฌ', '๐คฏ', '๐ณ', '๐ฅต', '๐ฅถ', '๐ฑ', '๐จ', '๐ฐ', '๐ฅ', '๐', '๐ค', '๐ค', '๐คญ', '๐คซ', '๐คฅ', '๐ถ', '๐', '๐', '๐ฌ', '๐', '๐ฏ', '๐ฆ', '๐ง', '๐ฎ', '๐ฒ', '๐ฅฑ', '๐ด', '๐คค', '๐ช', '๐ต', '๐ค', '๐ฅด', '๐คข', '๐คฎ', '๐คง', '๐ท', '๐ค', '๐ค', '๐ค', '๐ค ', '๐', '๐ฟ', '๐น', '๐บ', '๐คก', '๐ฉ', '๐ป', '๐', 'โ ๏ธ', '๐ฝ', '๐พ', '๐ค', '๐', '๐บ', '๐ธ', '๐น', '๐ป', '๐ผ', '๐ฝ', '๐', '๐ฟ', '๐พ']
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
        await ctx.send(message)
        #await ctx.message.delete(delay=5)

    #message on logging on (and enabling discord together)
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(815254981736529941)
        await channel.send('I have been awakened!')
        with open("token.json","r") as token:
            data = json.load(token)
            self.bot.togetherControl = await DiscordTogether(data.get("token"))

    #command used to activate discord together (possible activities are: youtube, poker, chess, betrayal, 
    # fishing, letter-league, word-snack, sketch-heads, spellcast, awkword and checkers)
    @commands.command(help="Creates discord acitivity of chosen type. Possible activities and their ids: \n Watch Together: youtube \n Poker Night: poker \n Chess in the Park: chess \n Betrayal.io: betrayal \n Fishington.io: fishing \n Letter League: letter-league \n Word Snack: word-snack \n Sketch Heads: sketch-heads, SpellCast: spellcast \n Awkword: awkword \n Checkers in the Park: checkers")
    async def together(self,ctx,activity):
        link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, activity)
        await ctx.send(f"Click the blue link!\n{link}")

    #if any message contains one of the defined words, bot responds appropriately
    #(as well as reacting with random emojis to some messages)
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "turbo" in ctx.content.lower():
            await ctx.reply(file=discord.File('./pics/so-true.gif'))
        if "jan" in ctx.content.lower():
            await ctx.add_reaction("๐ฏ")
            await ctx.add_reaction("๐ฆ")
            await ctx.add_reaction("๐ณ")
        roll = random.randrange(15)
        if roll == 1 and ctx.author != self.bot.user:
            await ctx.add_reaction(self.emojis[random.randrange(len(self.emojis))])