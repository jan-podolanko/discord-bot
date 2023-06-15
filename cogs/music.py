import asyncio
from discord.ext import commands
import discord
import youtube_dl
from discord.utils import get
import os

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.current_song = ""
        self.queue = []

    @commands.group(help="Commands related to music.")
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid music command.')
    
    # downloads yt_url to the audio directory
    def download_audio(self, yt_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.getcwd() + '/audio/%(title)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(yt_url)
                return info.get('title', None)
            except:
                info = ydl.extract_info(f"ytsearch:{yt_url}")['entries'][0]
                return info.get('title', None)

    def play_next(self, ctx):
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.queue) >= 1:
            
            vc.play(discord.FFmpegPCMAudio(f'audio/{self.queue[0]}.mp3'), after=lambda e: self.play_next(ctx))
            activity = discord.Activity(type=discord.ActivityType.listening, name=self.queue[0])
            asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing {self.queue[0]}."), self.bot.loop)
            asyncio.run_coroutine_threadsafe(self.bot.change_presence(status=discord.Status.online, activity=activity), self.bot.loop)
            self.current_song = self.queue[0]
            del self.queue[0]
        else:
            if not vc.is_playing():
                asyncio.run_coroutine_threadsafe(vc.disconnect(), self.bot.loop)
                asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."), self.bot.loop)
                act_vibing = discord.Activity(type=discord.ActivityType.listening, name="just vibing")
                asyncio.run_coroutine_threadsafe(self.bot.change_presence(status=discord.Status.idle, activity=act_vibing), self.bot.loop)


    @commands.command(help="Downloads and plays audio. Argument <song> is to be either a search term in quotes or a YouTube URL.")
    async def play(self, ctx, song):
        
        title = self.download_audio(song)
        self.queue.append(title)

        # gets voice channel of message author
        voice_channel = ctx.message.author.voice.channel
        # connect to vc
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if not vc:
            vc = await voice_channel.connect()


        if voice_channel == None:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")

        elif not vc.is_playing():
            # play audio by the mp3 title
            vc.play(discord.FFmpegPCMAudio(f'audio/{title}.mp3'), after=lambda e: self.play_next(ctx))
            await ctx.send(f'Now playing {title}.')
            self.current_song = title
            # change activity
            activity = discord.Activity(type=discord.ActivityType.listening, name=title)
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            del self.queue[0]
            
        else:
            await ctx.send(f'{title} queued.')
        
    @commands.command(help="Pauses song.")
    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        else:
            ctx.send("Not playing anything!")
        
    @commands.command(help="Resumes song.")
    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            voice_client.resume()
        else:
            ctx.send("Not playing anything!")

    @commands.command(help="Skips current song.")
    async def skip(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        else:
            ctx.send("Not playing anything!")

    @commands.command(help="Stops playing.")
    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            await voice_client.disconnect()
        else:
            ctx.send("Not playing anything!")

    @commands.command(help="Shows queue.")
    async def queue(self, ctx):
        if len(self.queue) > 0:
            await ctx.send(f"Currently playing: {self.current_song}.\nQueue:\n" + "".join([str(i) + ". " + str(x) + "\n" for i, x in enumerate(self.queue)]))
        elif self.current_song:
            await ctx.send(f"Currently playing: {self.current_song}.\nQueue empty.")
        else:
            await ctx.send("Queue empty.")

    @commands.command(help="Shows song currently playing.")
    async def current(self, ctx):
        if self.current_song:
            await ctx.send(f"Currently playing: {self.current_song}.")
        else:
            await ctx.send("Currently not playing anything.")