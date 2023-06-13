import asyncio
from discord.ext import commands
import discord
import youtube_dl
from discord.utils import get

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
            info = ydl.extract_info(yt_url)
            return info.get('title', None)
            """ vid_url = info.get('url', None)
            vid_id = info.get('id', None)
            vid_title = info.get('title', None)

            new_vid = {
                "id": vid_id,
                "title": vid_title,
                "url": vid_url
            }
        
            with open("./data/videos.json","r+") as vids_json:
                vids = json.load(vids_json)
                vids["vidoes"].append(new_vid)
                json.dump(vids,vids_json) """

    @commands.command(help="Plays audio from youtube url.")
    async def play(self, ctx, url):
        
        title = self.download_audio(url)
        
        # gets voice channel of message author
        voice_channel = ctx.message.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(f'audio/{title}.mp3'), after=lambda e: print('done', e))
            # Sleep while audio is playing.
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
        # Delete command after the audio is done playing.
        await ctx.message.delete()

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