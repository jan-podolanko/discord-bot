import discord
from discord.ext import commands
from datetime import date, time, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
        self.scheduler.start()

    #sends number of days since houseki no kuni hiatus :(
    @commands.command()
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        delta = date.today() - hiatus
        await ctx.send("It has been {} days since Land of the Lustrous went on hiatus. 😭".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    #function neccessary to send reminder messages
    async def rem(self,context,message):
        await context.send(f'Reminder: "{message}"')

    #sets up periodic reminders
    @commands.command()
    async def remind_daily(self, ctx, msg, time):
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, hour=h, minute=m)
        ctx.send(f'Added daily reminder - "{msg}" at {time}')
    
    @commands.command()
    async def remind_weekly(self, ctx, msg, time, week_day):
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day_of_week=week_day, hour=h, minute=m)
        ctx.send(f'Added weekly reminder - "{msg}" on every {week_day} at {time}')
    
    @commands.command()
    async def remind_monthly(self, ctx, msg, time, day_of_month):
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day=day_of_month, hour=h, minute=m)
        ctx.send(f'Added monthly reminder - "{msg}" on every {day_of_month} at {time}')
    
    @commands.command()
    async def remind_yearly(self, ctx, msg, time, date):
        h,m = [int(i) for i in time.split(':')]
        da,mo = [int(i) for i in date.split('.')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day=da, month=mo, hour=h, minute=m)
        ctx.send(f'Added yearly reminder - "{msg}" on {date} at {time}')

    #sets up a single reminder at specific date
    @commands.command()
    async def remind_once(self, ctx, msg, time, date):
        h,m = [int(i) for i in time.split(':')]
        da,mo,ye = [int(i) for i in date.split('.')]
        self.scheduler.add_job(self.rem,'date', args=[ctx,msg], name=msg, run_date=datetime(ye,mo,da,h,m,0))
        ctx.send(f'Added reminder - "{msg}"')

    #sends list of reminders
    @commands.command()
    async def list(self,ctx):
        if self.scheduler.get_jobs()==[]:
            await ctx.send("No reminders set currently.")
        else:
            jobs = [f"Name: {i.name}, Scheduled date: {i.next_run_time}\n" for i in self.scheduler.get_jobs()]
            await ctx.send("".join(jobs))
    
    #removes reminder by id
    @commands.command()
    async def remove(self,ctx,id):
        self.scheduler.remove_job(id)
        ctx.send(f"Succesfully removed reminder with id {id}")

    #modifies reminder by id
    #@commands.command()
    #async def modify(self,ctx,id,change):
    #    self.scheduler.modify_job(id,change)
    #    ctx.send(f"Succesfully modified reminder with id {id}")