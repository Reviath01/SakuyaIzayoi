import discord
from discord.ext import commands
import mysql.connector

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Shows server icon.", description="Shows server icon on a embed.")
    async def icon(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "icon":
                    await ctx.send('This command is disabled on this guild.')
                    return
        iconembed = discord.Embed(colour=discord.Colour.blue())
        iconembed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=iconembed)

    @commands.command(brief="Sends your message as spoiler.", description="Sends your message as spoiler.")
    async def spoiler(self, ctx, *, message = None):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "spoiler":
                    await ctx.send('This command is disabled on this guild.')
                    return
        if message == None:
            await ctx.send('You need to specify a message.')
            return
        else:
            spoilerembed = discord.Embed(colour=ctx.author.top_role.colour, description=f"|| {message} ||")
        await ctx.send(embed = spoilerembed)

    @commands.command(brief="Slap the user.", description="Slap the user.")
    async def slap(self, ctx, member : discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "slap":
                    await ctx.send('This command is disabled on this guild.')
                    return
        slapembed = discord.Embed(colour = ctx.author.top_role.colour, description=f"{ctx.author.mention} slaps <@{member.id}>")
        slapembed.set_image(url="https://images-ext-1.discordapp.net/external/79sCWyD-TmmyjFxlaQIxAkAANAfV529d-LDHNkGDM0M/%3Fitemid%3D10426943/https/media1.tenor.com/images/b6d8a83eb652a30b95e87cf96a21e007/tenor.gif")
        await ctx.send(embed=slapembed)

    @commands.command(brief="Sends your message as an embed.", description="Sends your message as an embed.")
    async def embed(self, ctx, *, message = None):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "embed":
                    await ctx.send('This command is disabled on this guild.')
                    return
        if message == None:
            await ctx.send('You need to specify a message.')
            return
        embed = discord.Embed(colour=ctx.author.top_role.colour, description=message)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(brief="Allows you to hug someone.", description="Allows you to hug someone.")
    async def hug(self, ctx, member : discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "hug":
                    await ctx.send('This command is disabled on this guild.')
                    return
        hugembed = discord.Embed(description=f"{ctx.author.mention} hugs <@{member.id}>", colour=discord.Colour.red())
        hugembed.set_image(url="https://i.pinimg.com/originals/4d/d7/49/4dd749423de10a319b5d9e8850bbace4.gif")
        await ctx.send(embed = hugembed)

    @commands.command(brief="Allows you to kiss someone.", description="Allows you to kiss someone.")
    async def kiss(self, ctx, member : discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT commandname FROM disabledcommands WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
                if y == "kiss":
                    await ctx.send('This command is disabled on this guild.')
                    return
        kissembed = discord.Embed(description=f"{ctx.author.mention} kisses {member.mention}", colour=0xff00eb)
        kissembed.set_image(url="https://media.tenor.com/images/d68747a5865b12c465e5dff31c65d5c2/tenor.gif")
        await ctx.send(embed = kissembed)

def setup(client):
    client.add_cog(Fun(client))
