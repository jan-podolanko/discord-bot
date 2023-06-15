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

    @commands.group(help="Contains commands related to music.")
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid music command.', delete_after=15)
    
    # downloads yt_url to the audio directory
    def download_audio(self, yt_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
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

    async def play_next(self, ctx):
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.queue) >= 1:
            # changes the current song value
            self.current_song = self.queue[0]
            # plays the next song in the queue
            vc.play(discord.FFmpegPCMAudio(f'audio/{self.queue[0]}.m4a'), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            # changes activity and sends message about the current song
            activity = discord.Activity(type=discord.ActivityType.listening, name=self.queue[0])
            await ctx.send(f"Now playing {self.queue[0]}.", delete_after=15)
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            # deletes the current song from queue
            del self.queue[0]
        else:
            #change activity and send message, then wait for 60 seconds before disconnecting
            act_vibing = discord.Activity(type=discord.ActivityType.listening, name="just vibing")
            await self.bot.change_presence(status=discord.Status.idle, activity=act_vibing)
            await ctx.send("No more songs in queue.", delete_after=15)
            await asyncio.sleep(60)
            await vc.disconnect()
                
    @music.command(help="Downloads and plays audio. Argument <song> is to be either a search term in quotes or a YouTube URL.")
    async def play(self, ctx, song):
        # downloads song and song title, then adds song to queue
        title = self.download_audio(song)
        self.queue.append(title)

        # gets voice channel of message author, then connects to vc
        voice_channel = ctx.message.author.voice.channel
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if not vc:
            vc = await voice_channel.connect()

        # sends message if command user isn't in voice channel
        if voice_channel == None:
            await ctx.send(str(ctx.author.name) + "is not in a channel.", delete_after=15)

        # if the bot isn't currently playing anything, plays the song
        elif not vc.is_playing():
            # plays audio by the m4a title; afterwards runs play_next function (which plays next song duh)
            vc.play(discord.FFmpegPCMAudio(f'audio/{title}.m4a'), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            await ctx.send(f'Now playing {title}.', delete_after=15)
            self.current_song = title

            # change activity
            activity = discord.Activity(type=discord.ActivityType.listening, name=title)
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            del self.queue[0]

        # if bot is currently playing a song, it only queues it up and sends this message
        else:
            await ctx.send(f'{title} queued.', delete_after=15)
        
    @music.command(help="Pauses song.")
    async def pause(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        else:
            ctx.send("Not playing anything!", delete_after=15)
        
    @music.command(help="Resumes song.")
    async def resume(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            voice_client.resume()
        else:
            ctx.send("Not playing anything!", delete_after=15)

    @music.command(help="Skips current song.")
    async def skip(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        else:
            ctx.send("Not playing anything!", delete_after=15)

    @music.command(help="Stops playing.")
    async def stop(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_playing():
            await voice_client.disconnect()
        else:
            ctx.send("Not playing anything!", delete_after=15)

    @music.command(help="Shows queue.")
    async def queue(self, ctx):
        if len(self.queue) > 0:
            await ctx.send(f"Currently playing: {self.current_song}.\nQueue:\n" + "".join([str(i) + ". " + str(x) + "\n" for i, x in enumerate(self.queue)]), delete_after=15)
        elif self.current_song:
            await ctx.send(f"Currently playing: {self.current_song}.\nQueue empty.", delete_after=15)
        else:
            await ctx.send("Queue empty.", delete_after=15)

    @music.command(help="Shows song currently playing.")
    async def current(self, ctx):
        if self.current_song:
            await ctx.send(f"Currently playing: {self.current_song}.", delete_after=15)
        else:
            await ctx.send("Currently not playing anything.", delete_after=15)
