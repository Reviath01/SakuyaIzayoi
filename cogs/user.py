import discord
from discord.ext import commands
import os
import psutil
import datetime, time
import platform
import sys
import mysql.connector

start_time = time.time()

class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('User commands are loaded!')

    @commands.command(brief="Send's latency of bot.", description="Send's latency of bot.")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}')

    @commands.command(invoke_without_command=True, brief="Send's user information.", description="Send's information about user (if you don't mention anyone, it will show yours).", pass_context=True, aliases=['userinfo', 'user-info'])
    async def whois(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        roles = [role.mention for role in member.roles[1:]]
        roles.append('@everyone')
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        warns3 = f"SELECT warnreason FROM warns WHERE memberid ='{member.id}' AND guildid = '{ctx.guild.id}'"
        mycursor.execute(warns3)
        myresult2 = mycursor.fetchall()
        if myresult2:
            for z in myresult2:
                t = str(z)[:-3][2:]
        else:
            t = "This user didn't warned on this guild"
        embed = discord.Embed(colour=member.top_role.colour, timestamp=ctx.message.created_at, title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Roles:", value=", ".join(roles))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        embed.add_field(name="Status:", value=str(member.status), inline=True)
        embed.add_field(name="Activity:", value=f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}", inline=True)
        embed.add_field(name="Bot:", value=member.bot)
        embed.add_field(name="Last Warn:", value=t)
        await ctx.send(embed=embed)

    @commands.command(brief="Fetch the profile picture of a user.", description="Fetch the profile picture of a user.", aliases=["pfp", "profile", "pp"])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        messageembed = discord.Embed(colour=ctx.author.top_role.colour, timestamp=ctx.message.created_at, title=f"Avatar of {member}")
        messageembed.set_image(url=member.avatar_url)
        await ctx.send(embed=messageembed)

    @commands.command(brief="Invite me!", description="My invite link.")
    async def invite(self, ctx):
        inviteembed = discord.Embed(colour=discord.Colour.red(), description=f"[Click here to invite me!](https://discordapp.com/oauth2/authorize?client_id=808385152601817169&scope=bot&permissions=8)")
        await ctx.send(embed=inviteembed)

    @commands.command(brief="Shows all roles.", description="Shows role list.", aliases=['role-list', 'rolelist', 'role_list'])
    async def roles(self, ctx):
        roles = [role.mention for role in ctx.guild.roles[1:]]
        roles.append('@everyone')
        rolesembed = discord.Embed(colour=discord.Colour.green(), description=", ".join(roles))
        await ctx.send(embed=rolesembed)

    @commands.command(invoke_without_command=True, brief="Shows my stats.", description="Shows my stats.", pass_context=True)
    async def stats(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        statembed = discord.Embed(colour=ctx.author.top_role.colour, title="My stats")
        statembed.add_field(name="Guild size", value=f"{len(self.client.guilds)}", inline=True)
        statembed.add_field(name="Ping", value=f"{round(self.client.latency * 1000)}", inline=True)
        statembed.add_field(name="Platform", value=f"{sys.platform}", inline=True)
        statembed.add_field(name="CPU percent", value=f"{psutil.cpu_percent()}%", inline=True)
        statembed.add_field(name="Uptime", value=text, inline=True)
        statembed.add_field(name="Category size", value=str(len(self.client.cogs)), inline=True)
        statembed.add_field(name="Commands size", value=str(len(self.client.commands)), inline=True)
        statembed.add_field(name="Discord.py version", value=str(discord.__version__), inline=True)
        statembed.add_field(name=f"Cached messages (in {text})", value=str(len(self.client.cached_messages)), inline=True)
        statembed.add_field(name="Python version", value=platform.python_version(), inline=True)
        await ctx.send(embed=statembed)

    @commands.command(brief="Shows server settings.", description="Shows server settings.", aliases=['server-settings', 'server_settings'])
    async def settings(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        chid = f"SELECT chid FROM leavech WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(chid)
        myresult = mycursor.fetchall()
        if myresult:
            for x in myresult:
                leavechannel = f"<#{str(x)[:-3][-18:]}> `({str(x)[:-3][-18:]})`"
        else:
            leavechannel = "Not setted"

        msg = f"SELECT msg FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(msg)
        myresult2 = mycursor.fetchall()
        if myresult2:
            for y in myresult2:
                leavemessage = str(y)[:-3][2:]
        else:
            leavemessage = "{mention} left the server."

        msg2 = f"SELECT msg FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(msg2)
        myresult3 = mycursor.fetchall()
        if myresult3:
            for t in myresult3:
                welcomemessage = str(t)[:-3][2:]
        else:
            welcomemessage = "Welcome to server {mention}"

        welcomech = f"SELECT chid FROM welcomech WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(welcomech)
        myresult4 = mycursor.fetchall()
        if myresult4:
            for z in myresult4:
                welcomechannel = f"<#{str(z)[:-3][-18:]}> `({str(z)[:-3][-18:]})`"
        else:
            welcomechannel = "Not setted"

        role = f"SELECT roleid FROM autorole WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(role)
        myresult5 = mycursor.fetchall()
        if myresult5:
            for aa in myresult5:
                autorole2 = f"<@&{str(aa)[:-3][2:]}> `({str(aa)[:-3][2:]})`"
        else:
            autorole2 = "Not setted"

        settedprefix = f"SELECT prefix FROM prefixes WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(settedprefix)
        myresult6 = mycursor.fetchall()
        if myresult6:
            for bb in myresult6:
                prefix = f"{str(bb)[:-3][2:]}"
        else:
            prefix = '!'

        loggingchannel = f"SELECT channelid FROM log WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(loggingchannel)
        myresult7 = mycursor.fetchall()
        if myresult7:
            for xx in myresult7:
                logchannel = f"<#{str(xx)[:-3][2:]}>"
        else:
            logchannel = "Not setted"

        embed = discord.Embed(colour=discord.Colour.red(), description=f"Settings of **{ctx.guild.name}**")
        embed.add_field(name="Leave channel", value=f"{leavechannel}")
        embed.add_field(name="Leave message", value=f"{leavemessage}")
        embed.add_field(name="Welcome channel", value=f"{welcomechannel}")
        embed.add_field(name="Welcome message", value=f"{welcomemessage}")
        embed.add_field(name="Autorole", value=f"{autorole2}")
        embed.add_field(name="Prefix", value=f"{prefix}")
        embed.add_field(name="Logging channel", value=f"{logchannel}")
        await ctx.send(embed=embed)
    
    @commands.command(brief="Sets you as afk", description="Sets you as afk")
    async def afk(self, ctx, *, reason = None):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        if reason == None:
            reason = "AFK"
        cursor = mydb.cursor()
        afk2 = "INSERT INTO afk (isafk, memberid, guildid) VALUES (%s, %s, %s)"
        value = ('true', ctx.author.id, ctx.guild.id)
        cursor.execute(afk2, value)
        mydb.commit()
        embed2 = discord.Embed(colour=discord.Colour.blue(), description=f"{ctx.author.mention} you are now afk with reason: \n`{reason}`")
        await ctx.send(embed=embed2)

def setup(client):
    client.add_cog(User(client))
