import numpy
import requests
import discord
from discord.ext import commands, tasks
from discord import app_commands
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageFont
from io import BytesIO
import datetime
import random

utc = datetime.timezone.utc
time = datetime.time(hour=5, minute=0, tzinfo=utc)

class color_commands(commands.Cog):
    def __init__(self, client):
        self.colorchoose.cancel()
        self.client = client
        self.colorchoose.start()

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    #daily color
    @tasks.loop(time=time)
    async def colorchoose(self):
        with open('assets/dailycolor.txt', 'w') as file:
            random_color = ('#' + ''.join(random.choice('ABCDEF0123456789') for i in range(6)))
            file.write(random_color)

    @colorchoose.before_loop
    async def before_water(self):
        await self.client.wait_until_ready()

    #bluescreen image error
    def bluescreen(self, text):
        image_error = Image.new('RGB', (200,200), f'#0000AA')
        draw = ImageDraw.Draw(image_error)
        font = ImageFont.truetype('assets/dosvga.ttf', size = 20)
        draw.text((4, 4), text, fill = '#AAAAAA', font = font)
        return image_error

    #generating color swatch
    def colorswatch(self, color):
        color = color.upper()
        if '#' not in color:
            color = '#' + color
        
        try:
            swatch = Image.new('RGB', (200,200), f'{color}')
        except:
            return 'FAILED'

        draw = ImageDraw.Draw(swatch)
        font = ImageFont.truetype('assets/dosvga.ttf', size = 30)
        draw.text((4, 23), f'{color}', fill = 'black', font = font)
        draw.text((4, 2), f'{color}', fill = 'white', font = font)
        return swatch

    #generating static
    def staticswatch(self, color1, color2):

        if '#' not in color1:
            color1 = '#' + color1
        if '#' not in color2:
            color2 = '#' + color2

        imarray = numpy.random.rand(200,200,3) * 255
        static = Image.fromarray(imarray.astype('uint8')).convert('L')
        try:
            static = ImageOps.colorize(image = static.convert('L'), black = color1, white = color2)
        except Exception as err:
            print(err)
            return 'FAILED'
        
        return static

    #lookup color
    @commands.hybrid_command(name = 'getcolor', description = 'lookup color, (using color hex)', aliases = ['gc'])
    @commands.cooldown(20,60,commands.BucketType.user)
    async def getcolor(self, ctx, *, color: str):

        swatch = self.colorswatch(color)
        
        if swatch == 'FAILED':
            swatch = self.bluescreen('Error!\nInvalid color\nFormat (#123456)')

        bytes = BytesIO()
        swatch.save(bytes, format='PNG')
        bytes.seek(0)

        dfile = discord.File(bytes, filename='swatch.png')
        await ctx.send(file = dfile)

    #random color
    @commands.hybrid_command(name = 'randomcolor', description = 'random color', aliases = ['rc'])
    @commands.cooldown(20,60,commands.BucketType.user)
    async def randomcolor(self, ctx):

        random_color = ('#' + ''.join(random.choice('ABCDEF0123456789') for i in range(6)))
        swatch = self.colorswatch(random_color)

        bytes = BytesIO()
        swatch.save(bytes, format='PNG')
        bytes.seek(0)

        dfile = discord.File(bytes, filename='random.png')
        await ctx.send(file = dfile)

    #color of the day
    @commands.hybrid_command(name = 'dailycolor', description = 'color of the day', aliases = ['cotd'])
    @commands.cooldown(20,60,commands.BucketType.user)
    async def dailycolor(self, ctx):
        with open('assets/dailycolor.txt') as file:
            color = file.read()
            color = color.strip('\n')

        swatch = self.colorswatch(color)
        if swatch == 'FAILED':
            swatch = self.bluescreen('Error!\nColor not chosen\nColor chosen at:\n12:00 PM cst')

        bytes = BytesIO()
        swatch.save(bytes, format='PNG')
        bytes.seek(0)

        dfile = discord.File(bytes, filename='dailycolor.png')
        await ctx.send(f'Today\'s color is {color}!', file=dfile)

    #static
    @commands.hybrid_command(name = 'static', description = 'two tone static', aliases = ['st'])
    @commands.cooldown(20,60,commands.BucketType.user)
    async def static(self, ctx, color1, color2):

        static = self.staticswatch(color1, color2)
        if static == 'FAILED':
            static = self.bluescreen('Error!\nInvalid color\nFormat (#123456)')

        bytes = BytesIO()
        static.save(bytes, format='PNG')
        bytes.seek(0)

        dfile = discord.File(bytes, filename='static.png')
        await ctx.send(file = dfile)

    #confetti
    @commands.hybrid_command(name = 'confetti', description = 'confetti static', aliases = ['cst'])
    @commands.cooldown(20,60,commands.BucketType.user)
    async def confetti(self, ctx):
        imarray = numpy.random.rand(200,200,3) * 255
        confetti = Image.fromarray(imarray.astype('uint8')).convert('RGBA')

        bytes = BytesIO()
        confetti.save(bytes, format='PNG')
        bytes.seek(0)

        dfile = discord.File(bytes, filename='confetti.png')
        await ctx.send(file = dfile)

async def setup(client):
    await client.add_cog(color_commands(client))

