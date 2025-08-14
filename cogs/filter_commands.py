import requests
import discord
from discord.ext import commands, tasks
from discord import app_commands
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from io import BytesIO
import datetime
import random

class filter_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.resize = (700, 700)

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #get last image
    async def get_last_image(self, ctx):
        asset = None
        image_data = None
        history = ctx.channel.history(limit=50)
        async for message in history:
            if message.attachments:
                url = message.attachments[0].url
                if url.startswith('https://cdn.discordapp.com'):
                    asset = message.attachments[0]
                    image_data = BytesIO(await asset.read())
                    break

            if message.embeds:
                url = message.embeds[0].url
                if url.startswith('https://cdn.discordapp.com'):
                    file = requests.get(url)
                    asset = file.content
                    image_data = BytesIO(asset)
                    break 

        return image_data


    #corrupt
    @commands.command(name='corrupt')
    @commands.cooldown(20, 60, commands.BucketType.user)
    async def corrupt(self, ctx, passes: int=None):
        if not passes:
            passes = 1

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image.save(bytes, format='JPEG')
            bytes.seek(0)
        
            image_data = bytes.read()
            image_data = bytearray(image_data)
        
        for i in range(passes):
            selection = random.randint(1500, len(image_data)-1)
            image_data[selection] = 0 # random.randint(1, 254)
        
        stream = BytesIO(image_data)
        with Image.open(stream).convert('RGB') as image:
            bytes.seek(0)
            image.save(bytes, format='JPEG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='corrupt.jpeg')
        await ctx.send(file = dfile)

    #2tone
    @commands.command(name='2tone')
    @commands.cooldown(20, 60, commands.BucketType.user)
    async def two_tone(self, ctx, color1=None, color2=None):

        if not color1:
            color1 = '#000000'
        if not color2:
            color2 = '#ffffff'

        if '#' not in color1:
            color1 = '#' + color1
        if '#' not in color2:
            color2 = '#' + color2

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            image_2tone = ImageOps.colorize(image = image.convert('L'), black = color1, white = color2)
            image_2tone.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='2tone.png')
        await ctx.send(file = dfile)

    #get profile picture
    @commands.hybrid_command(name='pfp', description='get a pfp')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def pfp(self, ctx, *, user: discord.User=None):
        if not user:
            pfp = ctx.author.avatar
        else:
            pfp = user.avatar

        if not pfp:
            await ctx.send('No profile picture found!')
            return

        await ctx.send(pfp)

    #get server profile picture
    @commands.hybrid_command(name='server-pfp', description='get the server pfp')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def server_pfp(self, ctx):
        pfp = ctx.guild.icon

        if not pfp:
            await ctx.send('No profile picture found!')
            return

        await ctx.send(pfp)

    #control
    @commands.command(name='control')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def control(self, ctx):

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='debug.png')
        await ctx.send(file = dfile)

    #image sharpen
    @commands.command(name='sharp')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def sharp(self, ctx, mode: str=None):
        
        if mode == 'light':
            intensity = 10
        elif mode == 'heavy':
            intensity = 100
        else:
            intensity = 50

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            sharpness_enhancer = ImageEnhance.Sharpness(image)
            image_sharp = sharpness_enhancer.enhance(intensity)
            image_sharp.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='sharp.png')
        await ctx.send(file = dfile)

    #invert
    @commands.command(name='invert')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def invert(self, ctx):

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            image_invert = ImageOps.invert(image)
            image_invert.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='invert.png')
        await ctx.send(file = dfile)

    #emboss
    @commands.command(name='emboss')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def emboss(self, ctx):

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            image_emboss = image.filter(ImageFilter.EMBOSS)
            image_emboss.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='emboss.png')
        await ctx.send(file = dfile)

    #vibe
    @commands.command(name='vibe')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def vibe(self, ctx, mode: str=None):

        if mode == 'light':
            intensity = 2
        elif mode == 'heavy':
            intensity = 25
        else:
            intensity = 10

        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            vibrance = ImageEnhance.Color(image)
            image_vibe = vibrance.enhance(intensity)
            image_vibe.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='vibe.png')
        await ctx.send(file = dfile)

    #brick
    @commands.command(name='brick')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def brick(self, ctx):

        image_data = await self.get_last_image(ctx)
        
        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('RGB') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = self.resize)
            brick = Image.open('assets/mask.png')
            image.paste(brick, (0,0), mask = brick)
            image.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='brick.png')
        await ctx.send(file = dfile)
        
    #1bit
    @commands.command(name='1bit')
    @commands.cooldown(20,60,commands.BucketType.user)
    async def one_bit(self, ctx):
        
        image_data = await self.get_last_image(ctx)

        if not image_data:
            await ctx.send('`no attachments`')
            return

        with Image.open(image_data).convert('1') as image:
            bytes = BytesIO()
            image = ImageOps.contain(image = image, size = (500, 500))
            image.save(bytes, format='PNG')
            bytes.seek(0)

        dfile = discord.File(bytes, filename='duotone.png')
        await ctx.send(file = dfile)

async def setup(client):
    await client.add_cog(filter_commands(client))
