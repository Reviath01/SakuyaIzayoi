import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun commands are loaded!')

    @commands.command(brief="Shows server icon", description="Shows server icon on a embed")
    async def icon(self, ctx):
        iconembed = discord.Embed(colour=discord.Colour.blue())
        iconembed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=iconembed)

    @commands.command(brief="Sends your message as spoiler", description="Sends your message as spoiler")
    async def spoiler(self, ctx, *, message = None):
        if message == None:
            await ctx.send('You need to specify a message')
            return
        else:
            spoilerembed = discord.Embed(colour=ctx.author.top_role.colour, description=f"|| {message} ||")
        await ctx.send(embed = spoilerembed)

    @commands.command(brief="Slap the user", description="Slap the user")
    async def slap(self, ctx, member : discord.Member):
        slapembed = discord.Embed(colour = ctx.author.top_role.colour, description=f"{ctx.author.mention} slaps <@{member.id}>")
        slapembed.set_image(url="https://images-ext-1.discordapp.net/external/79sCWyD-TmmyjFxlaQIxAkAANAfV529d-LDHNkGDM0M/%3Fitemid%3D10426943/https/media1.tenor.com/images/b6d8a83eb652a30b95e87cf96a21e007/tenor.gif")
        await ctx.send(embed=slapembed)

    @commands.command(brief="Sends your message as an embed", description="Sends your message as an embed")
    async def embed(self, ctx, *, message = None):
        if message == None:
            await ctx.send('You need to specify a message.')
            return
        embed = discord.Embed(colour=ctx.author.top_role.colour, description=message)
        await ctx.send(embed = embed)

    @commands.command(brief="Allows you to hug someone", description="Allows you to hug someone")
    async def hug(self, ctx, member : discord.Member):
        hugembed = discord.Embed(description=f"{ctx.author.mention} hugs <@{member.id}>", colour=discord.Colour.red())
        hugembed.set_image(url="https://i.pinimg.com/originals/4d/d7/49/4dd749423de10a319b5d9e8850bbace4.gif")
        await ctx.send(embed = hugembed)

def setup(client):
    client.add_cog(Fun(client))
