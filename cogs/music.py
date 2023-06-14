import asyncio
from discord.ext import commands
import discord
import youtube_dl
from discord.utils import get

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.playlist = []

    # downloads yt_url to the same directory from which the script runs
    def download_audio(self, yt_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'D:/proggy/discord bot/discord-bot/audio/%(title)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(yt_url)
                return info.get('title', None)
            except:
                info = ydl.extract_info(f"ytsearch:{yt_url}")['entries'][0]
                return info.get('title', None)


    @commands.command(help="Plays audio from youtube url.")
    async def play(self, ctx, url):
        
        title = self.download_audio(url)
        self.playlist.append(title)
        
        # gets voice channel of message author
        voice_channel = ctx.message.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name

            # connect to vc and play audio by the mp3 title
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(f'audio/{title}.mp3'), after=lambda e: print('done', e))

            # change activity
            activity = discord.Activity(type=discord.ActivityType.listening, name=title)
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            # sleep while audio is playing
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
        # delete command after the audio is done playing and change activity
        await ctx.message.delete()
        act_vibing = discord.Activity(type=discord.ActivityType.listening, name="just vibing")
        await self.bot.change_presence(status=discord.Status.idle, activity=act_vibing)

    @commands.command(help="Pauses audio.")
    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            voice_client.pause()
        
    @commands.command(help="Resumes audio.")
    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            voice_client.resume()

    @commands.command(help="Stops audio.")
    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            voice_client.stop()