import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from system.settings import CB_PREFIX

class message_reactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if not guild.system_channel:
            return

        channel = guild.system_channel
        with open('system/opt_in_features/welcome.txt', 'r') as file:
            text = file.read()
        if str(member.guild.id) not in text:
            return

        with open('assets/gifts.txt', 'r') as file:
            lines = file.readlines()
            gift = str(f'{lines[random.randint(0, len(lines)-1)]}')
            gift = gift.strip('\n')

        em = discord.Embed(description = f'**Welcome to {guild}, {member.mention}!**\n\n*{gift}*', color = discord.Colour.random())
        await channel.send(embed = em)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        message = str(ctx.content).lower()
        try:
            if 'vent' in ctx.channel.name.lower():
                return
            if 'serious' in ctx.channel.name.lower():
                return
        except AttributeError():
            pass
            
        if ctx.author == self.client.user:
            return

        with open('system/opt_in_features/reactions.txt', 'r') as file:
            file = file.read()

        if str(ctx.guild.id) not in file:
            return

        ilist = ['i am ', 'im ', 'i\'m ']
        for i in ilist:
            if random.randint(1, 30) != 30:
                break
            if message.startswith(i) and len(message) < 40:
                await ctx.channel.send(f'hi {message.split(i)[1]}, i\'m Capybasil')
        
        #the uwu channel
        if str(ctx.channel.id) == '1120475202975977595':
            uwu_response = ['uwu', 'its time for 1984 uwu', '*tazer buzzes cutely*', 'boowhomp']
            if 'uwu' not in message:
                await ctx.delete()
                await ctx.channel.send(random.choice(uwu_response))

        if message == f'{CB_PREFIX}baguette':
            await ctx.add_reaction('🥖')
    
        if 'i can still hear his voice' in message:
            await ctx.channel.send('gay gay homosexual gay')  
    
        if 'i can still hear her voice' in message:
            await ctx.channel.send('gay gay homosexual gay')
    
        if 'i can still hear their voice' in message:
            await ctx.channel.send('gay gay homosexual gay') 

        if 'success' in message:
            await ctx.add_reaction('<:basil_capitalism:1027385704457703454>')

        if 'yass' in message:
            await ctx.add_reaction('💅')

        if 'ball' in message:
            await ctx.add_reaction('<:Baller:1034151264474370158>')

        if 'wise' in message:
            await ctx.add_reaction('<:wise_tree:1027966495873052703>')

        if 'rebar' in message:
            await ctx.add_reaction('✨')

        if 'boowhomp' in message:
            await ctx.add_reaction('<:boowhomp:1142286491402383472>')

async def setup(client):
    await client.add_cog(message_reactions(client))
