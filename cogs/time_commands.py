import discord
from discord import app_commands
from discord.ext import commands, tasks
import subprocess
import random
import asyncio
import datetime
from system.settings import CB_OPERATORS

utc = datetime.timezone.utc
watertime = datetime.time(hour=18, minute=37, tzinfo=utc)
questiontime = datetime.time(hour=15, minute=0, tzinfo=utc)

class time_commands(commands.Cog):
    def __init__(self, client):
        self.operators = CB_OPERATORS
        self.water_channel = 1192526879094222878

        self.client = client
        self.water.cancel()
        self.water.start()
        self.question.cancel()
        self.question.start()

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #daily water
    @tasks.loop(time=watertime)
    async def water(self):
        channel = self.client.get_channel(self.water_channel)

        with open('assets/water.txt') as file:
            file = file.readlines()
            link = random.choice(file)
    
        em = discord.Embed(title = 'Remember to drink water', colour = discord.Colour.blue())
        em.set_image(url = link)
        
        await channel.send('<@&1192526992906653727>', embed=em)

    @water.before_loop
    async def before_water(self):
        await self.client.wait_until_ready()

    @commands.command(name='dailywater')
    async def dailywater(self, ctx, state: str):
        if str(ctx.author.id) not in self.operators:
            return

        if state == 'start':
            self.water.start()
            await ctx.send('`water loop started`')
        elif state == 'stop':
            self.water.cancel()
            await ctx.send('`water loop stopped`')
        else:
            await ctx.send(f'`{state} not found!')

    #daily water
    @tasks.loop(time=questiontime)
    async def question(self):
        channel = self.client.get_channel(1144453760819662878)
        await channel.send('<@&1192585494530363503>! It\'s time for a new question!')

    @question.before_loop
    async def before_question(self):
        await self.client.wait_until_ready()

    @commands.command(name='dailyquestion')
    async def dailyquestion(self, ctx, state: str):
        if str(ctx.author.id) not in self.operators:
            return

        if state == 'start':
            self.question.start()
            await ctx.send('`question loop started`')
        elif state == 'stop':
            self.water.cancel()
            await ctx.send('`question loop stopped`')
        else:
            await ctx.send(f'`{state} not found!')

    #tea command
    @commands.hybrid_command(name = 'tea', description = 'set a tea timer')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def tea(self, ctx,):
        await ctx.send('tea timer set')
        await asyncio.sleep(180)
        await ctx.send(f'{ctx.author.mention}! Your tea is done!')
   
    #noodle command
    @commands.hybrid_command(name = 'noodle', description = 'set a noodle timer')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def noodle(self, ctx,):
        await ctx.send('noodle timer set')
        await asyncio.sleep(300)
        await ctx.send(f'{ctx.author.mention}! Your noodles are done!')

    #remider command
    @commands.hybrid_command(name = 'remind', description = 'set a reminder')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def remind(self, ctx, amount: int, *, message: str):
        await ctx.send(f'sure, in {amount} seconds: \"{message}\"')
        await asyncio.sleep(amount)
        await ctx.send(f'{ctx.author.mention} {amount} seconds ago: \"{message}\"')

async def setup(client):
    await client.add_cog(time_commands(client))

