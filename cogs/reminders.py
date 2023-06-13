import discord
from discord.ext import commands
from datetime import date, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="Europe/Berlin")
        self.scheduler.start()

    #sends number of days since houseki no kuni hiatus :(
    @commands.command(help="Shows number of day since Houseki no Kuni went on hiatus. 😭")
    async def hiatus(self, ctx):
        hiatus = date(2020,12,25)
        next_chapter = date(2023,7,24)
        delta = date.today() + hiatus
        await ctx.send("Land of the Lustrous is no longe on hiatus 😃. {} days until the next chapter.".format(delta.days))
        await ctx.send(file=discord.File('./pics/sad.jpg'))

    #function neccessary to send reminder messages
    async def rem(self,context,message):
        await context.send(f'Reminder: "{message}"')

    @commands.group()
    async def remind(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid reminder command.')

    #sets up periodic reminders
    @remind.command(help="Sets up a daily reminder. Bot will send reminder every day at chosen hour. \n Argument <msg> must be included in quotes, like so: 'Remind me'. \n Argument <time> is to be formatted as 'h:m', for example: 16:45.")
    async def daily(self, ctx, msg, time):
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, hour=h, minute=m)
        await ctx.send(f'Added daily reminder - "{msg}" at {time}.')
    
    @remind.command(help="Sets up a weekly reminder. Bot will send reminder every week on chosen week day and hour. \n Argument <msg> must be included in quotes, like so: 'Remind me'. \n Argument <time> is to be formatted as 'h:m', for example: 16:45. \n Argument <day> is the full name of chosen day of the week - capitalization is irrelevant. Examples: 'Friday', 'sUnDaY'")
    async def weekly(self, ctx, msg, time, day):
        week_days={'monday':'mon', 'tuesday':'tue', 'wednesday':'wed', 'thursday':'thu', 'friday':'fri', 'saturday':'sat', 'sunday':'sun'}
        week_day = week_days[day.lower()]
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day_of_week=week_day, hour=h, minute=m)
        await ctx.send(f'Added weekly reminder - "{msg}" on every {day.lower()} at {time}.')
    
    @remind.command(help="Sets up a monthly reminder. Bot will send reminder every month on chosen day and hour. \n Argument <msg> must be included in quotes, like so: 'Remind me'. \n Argument <time> is to be formatted as 'h:m', for example: 16:45. \n Argument <day_of_month> is the chosen day of the month, for example: 30.")
    async def monthly(self, ctx, msg, time, day_of_month):
        h,m = [int(i) for i in time.split(':')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day=day_of_month, hour=h, minute=m)
        await ctx.send(f'Added monthly reminder - "{msg}" on every {day_of_month} at {time}.')
    
    @remind.command(aliases=["annually"], help="Sets up a yearly reminder. Bot will send reminder every year on chosen day, month and hour. \n Argument <msg> must be included in quotes, like so: 'Remind me'. \n Argument <time> is to be formatted as 'h:m', for example: 16:45. \n Argument <date> is to be formatted like 'day.month', for example: 26.12.")
    async def yearly(self, ctx, msg, time, date):
        h,m = [int(i) for i in time.split(':')]
        da,mo = [int(i) for i in date.split('.')]
        self.scheduler.add_job(self.rem,'cron', args=[ctx,msg], name=msg, day=da, month=mo, hour=h, minute=m)
        await ctx.send(f'Added yearly reminder - "{msg}" on {date} at {time}.')

    #sets up a single reminder at specific date
    @remind.command(help="Sets up a one-time reminder. Bot will send reminder once at chosen hour and on chosen day, month and year. \n Argument <msg> must be included in quotes, like so: 'Remind me'. \n Argument <time> is to be formatted as 'h:m', for example: 16:45. \n Argument <date> is to be formatted like 'day.month.year', for example: 26.12.2022")
    async def once(self, ctx, msg, time, date):
        h,m = [int(i) for i in time.split(':')]
        da,mo,ye = [int(i) for i in date.split('.')]
        self.scheduler.add_job(self.rem,'date', args=[ctx,msg], name=msg, run_date=datetime(ye,mo,da,h,m,0))
        await ctx.send(f'Added reminder - "{msg}" on {date} at {time}.')

    #sets up a reminder on an hourly interval
    @remind.command(help="Sets up a reminder on an interval. Argument <hours> is the number of hours to wait. \n Argument <start_date> is optional and it's default value is current date and time. \n If you want to specify date from which this reminder is to work, you must format it like this: '2010-10-10 09:30:00'")
    async def hourly(self, ctx, msg, hours, start_date=datetime.now()):
        self.scheduler.add_job(self.rem,'interval', args=[ctx,msg], name=msg, hours=int(hours), start_date=start_date)
        await ctx.send(f'Added reminder - "{msg}"')

    #sets up a reminder on an interval
    @remind.command(help="Sets up a reminder on an interval. Argument <no_of_days> is the number of days to wait. \n Argument <start_date> is optional and it's default value is current date and time. \n If you want to specify date from which this reminder is to work, you must format it like this: '2010-10-10 09:30:00'")
    async def interval(self, ctx, msg, no_of_days, start_date=datetime.now()):
        self.scheduler.add_job(self.rem,'interval', args=[ctx,msg], name=msg, days=int(no_of_days), start_date=start_date)
        await ctx.send(f'Added reminder - "{msg}"')

    #sends list of reminders
    @remind.command(help="Shows list of all reminders - their names, ids and next scheduled dates.")
    async def list(self,ctx):
        if self.scheduler.get_jobs()==[]:
            await ctx.send("No reminders set currently.")
        else:
            jobs = [f"Name: {i.name}, ID: {i.id}, Scheduled date: {i.next_run_time}\n" for i in self.scheduler.get_jobs()]
            await ctx.send("".join(jobs))
    
    #removes reminder by id
    @remind.command(aliases=["delete"], help="Removes reminder by id. To find the id of your reminder use !remind list")
    async def remove(self,ctx,id):
        self.scheduler.remove_job(id)
        await ctx.send(f"Succesfully removed reminder with id {id}")
    
    #modifies reminder by id
    @remind.command(enabled=False)
    async def modify(self,ctx,id,change):
        self.scheduler.get_job(id).modify(type=change)
        await ctx.send(f"Succesfully modified reminder with id {id}")
    