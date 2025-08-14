import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import random
from system.settings import CB_VERSION, CB_OPERATORS, CB_PREFIX, CB_ZABLOING_TRUSTED

class operator_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.version = CB_VERSION
        self.operators = CB_OPERATORS

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name=f'{CB_PREFIX} help'))
        
    @commands.command(name='errorlog')
    async def errorlog(self, ctx):
        if str(ctx.author.id) not in self.operators:
            return

        with open('system/error_log.txt', 'r') as file:
            file = file.readlines()
            if not file:
                error_log = 'No errors reported'
            else:
                error_log = ''.join(file)

            if len(error_log) >= 1000:
                error_log = 'error log is too long!\nplease clear cache or reboot capybasil'

            em = discord.Embed(title = 'Error log', description = f'```{error_log}```')
            await ctx.send(embed=em)

    @commands.command(name='halt')
    async def halt(self, ctx):
        if str(ctx.author.id) not in self.operators:
            return

        await ctx.send('Shutting down...\n')
        await self.client.change_presence(status=discord.Status.offline)
        time.sleep(1)
        exit()

    @commands.command(name='infolog')
    async def infolog(self, ctx):
        if str(ctx.author.id) not in self.operators:
            return
        with open('system/info_log.txt', 'r') as file:
            file = file.readlines()
            if not file:
                info_log = 'No system reports'
            else:
                info_log = ''.join(file)

            if len(info_log) >= 1000:
                info_log = 'system log is too long!\nplease clear cache or restart capybasil'

            em = discord.Embed(title = 'System log', description = f'```{info_log}```')
            await ctx.send(embed=em)

    @commands.command(name='clear-cache')
    async def clear_cache(self, ctx):
        with open('system/error_log.txt', 'w') as file:
            file.write('')
    
        with open('assets/dailycolor.txt', 'w') as file:
            file.write('UNCHOSEN')

        await ctx.send('```\ncleared\ndailycolor.txt\nerror_log.txt```')

    #dump config files
    @commands.command(name = 'dumpconfig')
    async def dumpconfig(self, ctx):
        if str(ctx.author.id) not in self.operators:
            return

        await ctx.send(file=discord.File(r'system/opt_in_features/reactions.txt'))
        await ctx.send(file=discord.File(r'system/opt_in_features/welcome.txt'))

    #changing status
    @commands.command(name = 'status')
    async def status(self, ctx, *, name):
        if str(ctx.author.id) not in self.operators:
            return

        await self.client.change_presence(activity=discord.Game(name=f'{name}'))
        await ctx.send(f'changed presence to {name}')

    #amianoperator
    @commands.command(name = 'amianoperator')
    async def amianoperator(self, ctx):
        if str(ctx.author.id) not in self.operators:
            await ctx.send('no')
            return

        await ctx.send('yea')

    #Syncing commands
    @commands.command(name='resync')
    async def resync(self, ctx):
        if str(ctx.author.id) not in self.operators:
            return

        try:
            synced = await self.client.tree.sync()
            await ctx.send(f'synced {len(synced)} command(s)')
        except Exception:
            await ctx.send(f'`{err}`')

    @commands.command(name = 'dailycolor_write')
    async def dcwrite(self, ctx, input: str=None):
        if str(ctx.author.id) not in self.operators:
            return

        if input == None:
            input = ('#' + ''.join(random.choice('ABCDEF0123456789') for i in range(6)))

        with open('assets/dailycolor.txt', 'w') as file:
            file.write(input)

        await ctx.send('daily color written')

    #dump zabloings into text file
    @commands.command(name='zabloing-dump')
    async def zabloing_dump(self, ctx):
        if str(ctx.author.id) not in CB_ZABLOING_TRUSTED:
            await ctx.send(file=discord.File(r'assets/zabloing.txt'))
    
async def setup(client):
    await client.add_cog(operator_commands(client))

