from discord.ext import commands
from datetime import date
import json, random, discord, requests

#quote commmands
class Quotes(commands.Cog):
    
    #group for all quote related commands
    @commands.group()
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid quote command.')
    
    #bot messages with random kanye quote from api
    @quote.command()
    async def kanye(self, ctx):
        quote = requests.get('https://api.kanye.rest/')
        json_quote = quote.json()
        await ctx.send('"{}" - Kanye West'.format(json_quote.get("quote")))

    #returns random quote from quotes.json file
    @quote.command()
    async def random(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            #choose random quote
            index = random.randrange(len(quotes))
            chosen_quote = quotes[index]

            await ctx.send(f'"{chosen_quote.get("quote")}" - {chosen_quote.get("author")}, {chosen_quote.get("date")}')

    #adds quote to json file
    @quote.command()
    async def add(self, ctx, quote, author, qdate=str(date.today())):
        new_quote = {
                "quote": quote,
                "author": author,
                "date": qdate
            }
        with open("./data/quotes.json","r+") as quotes_json:
            quotes = json.load(quotes_json)
            quotes["quotes"].append(new_quote)
            quotes_json.seek(0)
            json.dump(quotes,quotes_json)
            await ctx.send(f'Quote ""{quote}" - {author}, {qdate}" added.')

    #allows to download json file with quotes
    @quote.command()
    async def download(self, ctx):
        await ctx.send(file=discord.File("./data/quotes.json"))


    #sends all quotes by chosen author
    @quote.command()
    async def by(self, ctx, author):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]
            message = f"All quotes by: \n"
            for quote in quotes:
                if quote.get("author") == author:
                    message += f'"{quote.get("quote")}" - {quote.get("author")}, {quote.get("date")} \n'
                    
            await ctx.send(message)

    #lists all quote authors
    @quote.command()
    async def authors(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            authors_repeating = [dict.get("author") for dict in quotes if dict.get("author")]
            authors_nonrep = list(set(authors_repeating))

            await ctx.send('\n'.join(authors_nonrep))