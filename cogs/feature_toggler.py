import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from system.settings import CB_PREFIX

class feature_toggler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command(name='toggle')
    @commands.cooldown(10,60,commands.BucketType.user)
    @has_permissions(administrator=True)
    async def toggle(self, ctx, feature: str=None):
        if not ctx.guild:
            await ctx.send('this command is only available in servers!')
            return

        feature_list = ['patch', 'welcome', 'reactions']
        feature_desc = ['patch note announcements', 'welcome messages', 'capybasil message reactions']
        opt_list = ''

        if feature not in feature_list:
            for opt_file, item_desc in zip(os.listdir('system/opt_in_features'), feature_desc):
                with open(f'system/opt_in_features/{opt_file}', 'r') as file:
                    file = file.read()

                if str(ctx.guild.id) in file:
                    opt_list = opt_list + f'\n`{opt_file.split(".")[0]}` True\n{item_desc}\n'
                else:
                    opt_list = opt_list + f'\n`{opt_file.split(".")[0]}` False\n{item_desc}\n'

            desc = str(f'Use `{CB_PREFIX}toggle [feature]` to opt in/out of a feature\n{opt_list}')

            em = discord.Embed(title = f'Feature toggler', description = desc,)
            await ctx.send(embed = em)
            return

        with open(f'system/opt_in_features/{feature}.txt', 'r') as file:
            file = file.read()
            server_list = file.split('~~~')

        for item in server_list:
            if str(ctx.guild.id) in item:
                server_list.remove(item)
                await ctx.send(f'feature `{feature}` has been disabled for {ctx.guild}')
                break
        else:
            server_list.append(str(ctx.guild.id))
            await ctx.send(f'feature `{feature}` has been enabled for {ctx.guild}')


        newfile = '~~~'.join(server_list)
        with open(f'system/opt_in_features/{feature}.txt', 'w') as file:
            file.write(newfile)

async def setup(client):
    await client.add_cog(feature_toggler(client))
