from discord.ext import commands
from datetime import date
import json, random, discord, requests

#quote commmands
class Quotes(commands.Cog):
    
    #bot messages with random kanye quote from api
    @commands.command()
    async def kanye(self, ctx):
        quote = requests.get('https://api.kanye.rest/')
        json_quote = quote.json()
        await ctx.send('"{}" - Kanye West'.format(json_quote.get("quote")))

    #returns random quote from quotes.json file
    @commands.command()
    async def rand_quote(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            #choose random quote
            index = random.randrange(len(quotes))
            chosen_quote = quotes[index]

            await ctx.send(f'"{chosen_quote.get("quote")}" - {chosen_quote.get("author")}, {chosen_quote.get("date")}')

    #adds quote to json file
    @commands.command()
    async def add_quote(self, ctx, quote, author, qdate=str(date.today())):
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
    @commands.command()
    async def download_quotes(self, ctx):
        await ctx.send(file=discord.File("./data/quotes.json"))


    #sends all quotes by chosen author
    @commands.command()
    async def quotes_by(self, ctx, author):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]
            message = f"All quotes by: \n"
            for quote in quotes:
                if quote.get("author") == author:
                    message += f'"{quote.get("quote")}" - {quote.get("author")}, {quote.get("date")} \n'
                    
            await ctx.send(message)

    #lists all quote authors
    @commands.command()
    async def quote_authors(self, ctx):
        with open("./data/quotes.json","r") as quotes_json:
            quotes = json.load(quotes_json)["quotes"]

            authors_repeating = [dict.get("author") for dict in quotes if dict.get("author")]
            authors_nonrep = list(set(authors_repeating))

            await ctx.send('\n'.join(authors_nonrep))

