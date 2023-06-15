from discord.ext import commands
from datetime import date
import json, random, discord, requests

#quote commmands
class Quotes(commands.Cog):
    
    #group for all quote related commands
    @commands.group(help="Commands related to quotes.")
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid quote command.', delete_after=15)
    
    #sends random kanye quote from api
    @quote.command(aliases=["ye"], help="Sends a random kanye quote.")
    async def kanye(self, ctx):
        quote = requests.get('https://api.kanye.rest/')
        json_quote = quote.json()
        await ctx.send('"{}" - Kanye West'.format(json_quote.get("quote")))

    #sends random quote from saved quotes (quotes.json file)
    @quote.command(help="Sends random quote from previously saved quotes.")
    async def random(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            #choose random quote
            index = random.randrange(len(quotes))
            chosen_quote = quotes[index]

            await ctx.send(f'"{chosen_quote.get("quote")}" - {chosen_quote.get("author")}, {chosen_quote.get("date")}')

    #adds quote to json file
    @quote.command(help="Adds quote to random quote list. \n Argument <quote> must be included in quotes, for example: 'I can resist everything except temptation.' \n Argument <author> must be included in quotes in the case it's longer than one word, like so: 'Oscar Wilde' \n Argument <date> is optional and defaults to today's date. It must be included in quotes in the case it's longer than one word - 16.12.2022 is okay, but 'a few days ago' would need to be in quotes.")
    async def add(self, ctx, quote, author, date=str(date.today())):
        new_quote = {
                "quote": quote,
                "author": author,
                "date": date
            }
        with open("./data/quotes.json","r+") as quotes_json:
            quotes = json.load(quotes_json)
            quotes["quotes"].append(new_quote)
            quotes_json.seek(0)
            json.dump(quotes,quotes_json)
            await ctx.send(f'Quote ""{quote}" - {author}, {date}" added.')

    #allows to download json file with quotes
    @quote.command(help="Sends file with all saved quotes in the json file format.")
    async def download(self, ctx):
        await ctx.send(file=discord.File("./data/quotes.json"))

    #sends all quotes by chosen author
    @quote.command(help="Shows all quotes by specific author.")
    async def by(self, ctx, author):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]
            message = f"All quotes by {author}: \n"
            for quote in quotes:
                if quote.get("author") == author:
                    message += f'"{quote.get("quote")}" - {quote.get("author")}, {quote.get("date")} \n'
                    
            await ctx.send(message)

    #lists all quote authors
    @quote.command(help="Shows list of all quote authors.")
    async def authors(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            authors_repeating = [dict.get("author") for dict in quotes if dict.get("author")]
            authors_nonrep = list(set(authors_repeating))

            await ctx.send('\n'.join(authors_nonrep))