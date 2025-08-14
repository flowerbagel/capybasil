#!/usr/bin/python3

import discord
from discord.ext import commands
import os
import asyncio
from rich.console import Console
import time
import datetime
from system.settings import CB_PREFIX, CB_VERSION, CB_OPERATORS, CB_TOKEN, CB_DEVMODE

TOKEN = CB_TOKEN

console = Console()
version = CB_VERSION
prefix = CB_PREFIX
totalcogs = ['color_commands',
             'filter_commands',
             'general_commands',
             'zabloing_commands',
             'time_commands', 
             'message_reactions',
             'feature_toggler',
             ]

# clear logs
def logreset():
    with open('system/error_log.txt', 'w') as file:
        console.log('✔ Error log cleared', style = 'bold cyan')

    with open('system/info_log.txt', 'w') as file:
        console.log('✔ Info log cleared', style = 'bold cyan')

    with open('assets/dailycolor.txt', 'w') as file:
        file.write('UNCHOSEN')
        console.log('✔ Daily color cleared', style = 'bold cyan')
# main
def main():
    client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())
    client.remove_command('help')

    os.system('clear')
    print(' ██████╗ █████╗ ██████╗ ██╗   ██╗██████╗  █████╗ ███████╗██╗██╗    ') 
    print('██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██║██║    ') 
    print('██║     ███████║██████╔╝ ╚████╔╝ ██████╔╝███████║███████╗██║██║    ') 
    print('██║     ██╔══██║██╔═══╝   ╚██╔╝  ██╔══██╗██╔══██║╚════██║██║██║    ') 
    print('╚██████╗██║  ██║██║        ██║   ██████╔╝██║  ██║███████║██║███████╗')
    print(' ╚═════╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚══════╝')

    if CB_DEVMODE:
        print(f'    v{version} DEVMODE\n')
    else:
        print(f'    v{version}\n')

    #startup
    @client.event
    async def on_ready():
        console.log('* attempting sync...', style = 'bold cyan')
        try:
            synced = await client.tree.sync()
            console.log('✔ Successfully logged in as {0.user},'.format(client), style = 'bold')
            console.log(f'✔ Synced {len(synced)} command(s)\n', style = 'bold')
        except Exception as err:
            console.log(f'✘ Fatal error! {err}', style = 'bold red')
            exit()

    #processing commands
    @client.event
    async def on_message(message):
        if message.content.lower().startswith(prefix):
            message.content = message.content[:4].lower() + message.content[4:]
            await client.process_commands(message)

    #error handling and logging
    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"`✘ chill bestie! {error}`", ephemeral=True)
            return

        console.log(f"✘ {error}", style = 'bold red')
        await ctx.send(f"`✘ {error}`", ephemeral=True)
        
        with open('system/error_log.txt', 'a') as file:
            file.write(f'\n{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, [{ctx.command}], [{error}]')

    #command logging
    @client.event
    async def on_command(ctx):
        if not ctx.guild:
            guild = 'direct message'
        else:
            guild = ctx.guild

        console.log(f'✔ Command Recieved "{ctx.command}", ({ctx.author}, {guild})', style = 'bold cyan')

    #load cogs on startup
    async def load():
        try:
            await client.load_extension(f"system.operator_commands")
            console.log(f'✔ cog (operator_commands) loaded', style = 'bold cyan')
        except Exception as error:
            console.log(error)
            console.log(f'✘ cog (operator_commands) error!', style = 'bold red')

        for cog in totalcogs:
            try:
                await client.load_extension(f"cogs.{cog}")
                console.log(f'✔ cog ({cog}) loaded', style = 'bold cyan')
            except commands.ExtensionNotFound:
                console.log(f'✘ cog ({cog}) not found!', style = 'bold red')
            except Exception as error:
                console.log(error)
                console.log(f'✘ cog ({cog}) error!', style = 'bold red')

    #manual cog loading
    @client.command(name='cogload')
    async def cogload(ctx, selection):
        if str(ctx.author.id) not in CB_OPERATORS:
            return
        
        output = ''
        if selection.lower() == '*':
            for cog in totalcogs:
                try:
                    await client.load_extension(f'cogs.{cog}')
                    output = output + str(f'✔ cog {cog} loaded\n')
                except commands.ExtensionAlreadyLoaded:
                    output = output + str(f'✘ cog {cog} already loaded\n')
                except Exception:
                    output = output + str(f'✘ cog {cog} error!\n')
            await ctx.send(f'```{output}```')
            return

        if str(selection) not in totalcogs:
            await ctx.send(f'```? cog {selection} not in list, proceeding```')

        try:
            await client.load_extension(f"cogs.{selection}")
            output = output + str(f'✔ cog {selection} loaded\n')
        except commands.ExtensionAlreadyLoaded:
            output = output + str(f'✘ cog {selection} already loaded\n')
        except Exception:
            output = output + str(f'✘ cog {selection} error!\n')
        await ctx.send(f'```{output}```')

    #manual cog unloading
    @client.command(name='cogunload')
    async def cogunload(ctx, selection):
        if str(ctx.author.id) not in CB_OPERATORS:
            return

        output = ''
        if selection.lower() == '*':
            for cog in totalcogs:
                try:
                    await client.unload_extension(f'cogs.{cog}')
                    output = output + str(f'✔ cog {cog} unloaded\n')
                except Exception:
                    output = output + str(f'✘ cog {cog} already unloaded\n')
            await ctx.send(f'```{output}```')
            return

        if str(selection) not in totalcogs:
            await ctx.send(f'```? cog {selection} not in list, proceeding```')

        try:
            await client.unload_extension(f"cogs.{selection}")
            output = output + str(f'✔ cog {selection} unloaded\n')
        except Exception:
            output = output + str(f'✘ cog {selection} error\n')

        await ctx.send(f'```{output}```')

    # cog checking
    @client.command(name='cogcheck')
    async def cogcheck(ctx):
        if str(ctx.author.id) not in CB_OPERATORS:
            return

        cogchecklist = ''
        for i in totalcogs:
            try:
                await client.load_extension(f"cogs.{i}")
            except commands.ExtensionNotFound:
                cogchecklist = str(cogchecklist) + str(f'⚫ cog {i} not found\n')
            except commands.ExtensionAlreadyLoaded:
                cogchecklist = str(cogchecklist) + str(f'🟢 cog {i} online\n')
            else:
                cogchecklist = str(cogchecklist) + str(f'🔴 cog {i} error\n')
                await client.unload_extension(f"cogs.{i}")

        em = discord.Embed(title='Cog Status:', description=cogchecklist)
        await ctx.send(embed=em)

    async def start():
        logreset()
        await load()
        await client.start(TOKEN)

    asyncio.run(start())

if __name__ == '__main__':
    main()
