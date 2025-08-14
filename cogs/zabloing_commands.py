import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
from system.settings import CB_OPERATORS, CB_ZABLOING_TRUSTED

class zabloing_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.trusted_servers = CB_ZABLOING_TRUSTED
#        self.zabloing_logging_channel = 
        self.operators = CB_OPERATORS
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #Adding a zabloing
    @commands.hybrid_command(name='zabloing-add', description='Add a zabloing')
    @app_commands.describe(zabloing = 'Your zabloing:')
    @commands.cooldown(10,300,commands.BucketType.user)
    async def zabloing_add(self, ctx, *, zabloing: str):
        if str(ctx.guild.id) not in self.trusted_servers:
            return

        if '~~~' in str(zabloing).lower():
            await ctx.send('Cannot write zabloing! "~~~" is used for formatting', ephemeral=True)
            return

        if str(zabloing) == '** **':
            await ctx.send('Cant write empty zabloing!', ephemeral=True)
            return

        username = str(ctx.author)
        with open('assets/zabloing.txt', 'r') as file:
            text = file.read()
            text = text.split('~~~')
            number = int(len(text))

        with open('assets/zabloing.txt', 'a') as file:
            zabloing = str(f'\n~~~\n*Zabloing #{number}: ({datetime.date.today()}, added by {username})*\n{str(zabloing)}')
            file.write(zabloing)

        await ctx.send(f'Zabloing added successfully! \n{zabloing[5:]}')

#        channel = self.client.get_channel(self.zabloing_logging_channel)
#        em = discord.Embed(title = f'zabloing added', description = str(f'```{zabloing.split("~~~")[1]}```'), color=discord.Colour.green())
#        await channel.send(embed = em)

    #Gets a zabloing
    @commands.hybrid_command(name='zabloing', description='Shows a random zabloing')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def zabloing(self, ctx, number=None):

        if str(ctx.guild.id) not in self.trusted_servers:
            return

        with open('assets/zabloing.txt', 'r') as file:
            text = file.read()
            text = text.split('~~~')

        if not number:
            await ctx.send(random.choice(text))
        else:
            await ctx.send(text[int(number)])


    #Shows number of total zabloings
    @commands.hybrid_command(name='zabloing-count', description='Shows total number of zabloings')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def zabloing_count(self, ctx):
        if str(ctx.guild.id) not in self.trusted_servers:
            return

        with open('assets/zabloing.txt', 'r') as file:
            text = file.read()
            text = text.split('~~~')

        await ctx.send(f'there are {len(text)-1} zabloings in the great zabloing.txt')

    #Searching zabloings
    @commands.hybrid_command(name='zabloing-search', description='search for a zabloing')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def zabloing_search(self, ctx, *, query: str):
        if str(ctx.guild.id) not in self.trusted_servers:
            return

        results = ''

        with open('assets/zabloing.txt', 'r') as file:
            text = file.read()
            text = text.split('~~~')

        for item in text:
            if query.lower() in item.lower():
                results = results + item

        if results == '':
            await ctx.send('`No results`')

        elif len(results) > 3000:
            await ctx.send('`Too many results`')

        else:
            em = discord.Embed(title = f'Search results for {query}', description = results, colour = discord.Colour.random())
            await ctx.send(embed=em)

async def setup(client):
    await client.add_cog(zabloing_commands(client))
