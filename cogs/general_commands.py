import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions
import subprocess
import random
import asyncio
import datetime
from io import BytesIO
from system.settings import CB_VERSION, CB_ZABLOING_TRUSTED

class general_commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # making a progress bar
    def make_bar(self, percentage):
        progress = ''
        unfilled = 10 - round(percentage/10)
        filled = 10 - unfilled

        for i in range(filled):
            progress = progress + '#'
        for i in range(unfilled):
            progress = progress + '  '
        return progress, percentage

    #help command
    @commands.hybrid_command(name='help', description='help page')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def help(self, ctx, query=None):

        with open('system/error_log.txt', 'r') as file:
            errors = 0
            text = file.readlines()
            errors = len(text)
        
        with open('assets/help.txt', 'r') as file:
            text = file.read()
            text = text.split('~~~')

        if not query:
            if ctx.guild:
                if str(ctx.guild.id) in CB_ZABLOING_TRUSTED:
                    desc = str(text[0].format(zabloing='> for info about zabloings use `help zabloing`'))
                else:
                    desc = str(text[0].format(zabloing=''))
            else:
                desc = str(text[0].format(zabloing=''))

        elif query == 'general':
            desc = str(text[1])
        elif query == 'time':
            desc = str(text[2])
        elif query == 'image':
            desc = str(text[3])
        elif query == 'zabloing':
            desc = str(text[4])
        else:
            return

        em = discord.Embed(title = f'Capybasil help', description = desc,)

        if query is None:
            em.add_field(name = 'version', value = CB_VERSION)
            em.add_field(name = 'errors', value = errors)

        await ctx.send(embed = em)

    #uptime command
    @commands.hybrid_command(name='uptime', description='displays capybasil server uptime')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def uptime(self, ctx, query=None):
        if not query:
            uptime = subprocess.run(['uptime', '-p'], stdout = subprocess.PIPE)
            uptime = str(uptime.stdout)[5:-3]
        if query == 'days':
            uptime = subprocess.run(['uptime'], stdout = subprocess.PIPE)
            uptime = str(uptime.stdout)[2:-3]
        await ctx.send(f'server uptime: {uptime}')

    #sort
    @commands.hybrid_command(name='sort', description='sort a list of words in alphabetical order')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def alphabetize(self, ctx, *, words: str):
        words = words.lower()
        word_list = words.split(' ')
        word_list = sorted(word_list)
        word_list = '\n'.join(word_list)
        await ctx.send(f'ding!\n```\n{word_list}```')

    @commands.hybrid_command(name='echo', description='make capybasil send a message to a channel')
    @has_permissions(administrator=True)
    @commands.cooldown(20,60,commands.BucketType.user)
    async def echo(self, ctx, target_channel: int, *, message: str):
        channel = self.client.get_channel(target_channel)
        if channel.guild != ctx.guild:
            await ctx.send('echoed message must be in the same server!')
            return
        await channel.send(str(message))

    @commands.hybrid_command(name='basil', description='basil')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def basil(self, ctx):
        await ctx.send('it\'s me!')

    #Ping command
    @commands.hybrid_command(name='ping', description='Pings capybasil')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f'*thonk* ({round(self.client.latency * 1000)}ms)')

    #Test command
    @commands.hybrid_command()
    @commands.cooldown(20,60,commands.BucketType.user)
    async def test(self, ctx):
        await ctx.send(f'Hello world!\n')

    #youtube link scrubinator
    @commands.hybrid_command()
    @commands.cooldown(20,60,commands.BucketType.user)
    async def scrub(self, ctx, link: str):
        time_code = ''
        youtube_words = ['https://youtu.be', 'https://youtube.com', 'https://www.youtube.com']
        link_is_youtube = False

        for word in youtube_words:
            if word in link:
                link_is_youtube = True
                break

        if not link_is_youtube:
            return

        if 'si=' not in link:
            await ctx.send('this link already appears clean!')
            return
    
        if '&t=' in link:
            time_code = link.split('&')[-1]
    
        link = link.split('?')
    
        for section in link:
            if 'si=' in section:
                link.remove(section)
                break

        link = '?'.join(link)

        if time_code != '':
            link = link + '&' + time_code
    
        await ctx.send(f'link scrubbed!\n{link}')

    #rock paper scissors
    @commands.hybrid_command(name='rps')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def rps(self, ctx, *, selection=None):
        choices = ['rock', 'paper', 'scissors']
        if not selection:
            selection = 'nothing'

        selection = selection.lower()
        computer_selection = random.choice(choices)

        if 'men' in selection:
            await ctx.send(f'You chose *{selection}*\nI *love* men, you win.')
            return

        if selection == 'discord developer badge':
            await ctx.send(f'<:basil_nervous:1124394209030451280> are you the reason discord has to tell people not to run random .exe programs on their computers?')
            return

        if selection not in choices:
            await ctx.send(f'You chose *{selection}*\nballs.')
            return

        # actual rock paper scissors
        if selection == computer_selection:
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nIts a tie!')
            return

        if selection == 'rock' and computer_selection == 'paper':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou lose!')
            return
        if selection == 'paper' and computer_selection == 'scissors':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou lose!')
            return
        if selection == 'scissors' and computer_selection == 'rock':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou lose!')
            return

        if selection == 'paper' and computer_selection == 'rock':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou win!')
            return
        if selection == 'scissors' and computer_selection == 'paper':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou win!')
            return
        if selection == 'rock' and computer_selection == 'scissors':
            await ctx.send(f'You chose *{selection}*\nI chose *{computer_selection}*\nYou win!')
            return


    #meter command
    @commands.hybrid_command(name='meter')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def meter(self, ctx, subject, user=None):
        bar, percentage = self.make_bar(random.randint(1, 100))
        if user == None:
            user = ctx.author.mention

        if user == '<@842879465709109289>' and str(subject) == 'gay':
            percentage = 9999999999
            bar = '##########'
        await ctx.send(f'{user}\'s {subject} meter\n[{bar}] {percentage}%')

    #demise command
    @commands.hybrid_command(name='demise', description='Cause the unfortunate demise of someone')
    @app_commands.describe(target = 'Who do you want to demise?')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def demise(self, ctx, *, target: str=None):
        username = str(ctx.author).split('#')[0]
        if target is None:
            target = username
        with open('assets/deaths.txt', 'r') as file:
            lines = file.readlines()
            await ctx.send(lines[random.randint(0, len(lines)-1)].format(target = target, username = username))

    #Rebar command
    @commands.hybrid_command(name='rebar', description='rebar')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def rebar(self, ctx):
        yass = random.randint(0, 10)
        if yass == 10:
            em = discord.Embed(colour = discord.Colour.red(), title = '✨rebar✨')
            em.set_image(url='https://cdn.discordapp.com/attachments/1042472356448313386/1042472654873051147/ReBaR.jpg')
            await ctx.send(embed=em)
        elif yass == 9:
            em = discord.Embed(colour = discord.Colour.orange(), title = 'american style deepfried rebar')
            em.set_image(url='https://cdn.discordapp.com/attachments/1042472356448313386/1042472731029020772/deepfry.png')
            await ctx.send(embed=em)
        else:
            em = discord.Embed(colour = discord.Colour.blue(), title = 'rebar')
            em.set_image(url='https://cdn.discordapp.com/attachments/1042472356448313386/1042472654646546502/rebar.jpg')
            await ctx.send(embed=em)

    #reba command
    @commands.command(name='reba')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def reba(self, ctx):
        em = discord.Embed(colour = discord.Colour.green(), title = 'reba')
        em.set_image(url='https://cdn.discordapp.com/attachments/1042472356448313386/1142282984003747871/reba.jpg')
        await ctx.send(embed=em)
    
    #boowhomp command
    @commands.command(name='boowhomp')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def boowhomp(self, ctx):
        em = discord.Embed(colour = discord.Colour.yellow(), title = 'boowhomp')
        em.set_image(url='https://media.discordapp.net/attachments/1042472356448313386/1142284586500497469/debug.png?width=759&height=427')
        await ctx.send(embed=em)
       
    #Random number command
    @commands.hybrid_command(name='roll', description='Picks a random number')
    @app_commands.describe(number = 'Picks a random number')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def roll(self, ctx, number: int):
        result = random.randint(1, int(number))
        await ctx.send(f'Rolling ({number}),\nYou rolled {result}!')

    #Gift command
    @commands.hybrid_command(name='gift', description='Capybasil gives you a gift')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def gift(self, ctx):
        with open('assets/gifts.txt', 'r') as file:
            file = file.readlines()
            await ctx.send(f'{random.choice(file)}')

    #Motivation command
    @commands.hybrid_command(name='motivation', description='Capybasil gives you some motivation')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def motivation(self, ctx):
        with open('assets/motivation.txt', 'r') as file:
            file = file.readlines()
            await ctx.send(f'{random.choice(file)}')

    #Door command
    @commands.hybrid_command(name='door', description='Capybasil gives you a door')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def door(self, ctx):
        with open('assets/doors.txt', 'r') as file:
            lines = file.readlines()
            await ctx.send(f'{lines[random.randint(0, len(lines)-1)]}')

    #A command that does nothing
    @commands.hybrid_command(description='This command does nothing')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def nothing(self, ctx):
        if random.randint(0, 15) == 15:
            await ctx.send('why are you like this')
        else:
            await ctx.send('This command does nothing')

    #Cry command
    @commands.hybrid_command(description='Allows you to cry with capybasil')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def cry(self, ctx):
        await ctx.send(f'I was crying alone in an alley, {ctx.author.mention} walked up and crew too, we both crode <:basil_cry:1027376339717734420>')

    #Invite command
    @commands.hybrid_command(description='Invite for capybasil')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def invite(self, ctx):
        await ctx.send(f'https://discord.com/api/oauth2/authorize?client_id=1026874054239600712&permissions=277025770560&scope=bot%20applications.commands')

    #case command
    @commands.hybrid_command(name='case', description='ReTurNs iNPuT lIKE ThiS')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def case(self, ctx, *, input):
        message = ''
        for i in input:
            if random.randint(0, 1) == 1:
                message = message + i.lower()
            else:
                message = message + i.upper()
        await ctx.send(message) 

    #clap command
    @commands.hybrid_command(name='clap', description='RETURNS👏INPUT👏LIKE👏THIS')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def clap(self, ctx, *, input):
        input = input.upper()
        input = input.split(' ')
        message = '👏'.join(input)
        await ctx.send(message)

    #Link to DOOM shareware
    @commands.command()
    @commands.cooldown(20,60,commands.BucketType.user)
    async def doom(self, ctx):
        await ctx.send('https://www.doomworld.com/idgames/idstuff/doom/doom19s')

async def setup(client):
    await client.add_cog(general_commands(client))
