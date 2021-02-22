import discord
from discord.ext import commands
import json
import mysql.connector

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation commands are loaded!')

    @commands.command(brief="Ban the user.", description="Allow's you to ban the user.")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.User, *, reason = None):
        if member == ctx.message.author:
            await ctx.send('You can\'t ban yourself.')
            return
        if reason == None:
            reason = "Unspecified"
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"Banned {member.mention}!")

    @commands.command(brief="Kick the user.", description="Allow's you to kick the user.")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.User, *,reason = None):
        if member == ctx.message.author:
            await ctx.send('You can\'t kick yourself.')
            return
        if reason == None:
            reason = "Unspecified"
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"Kicked {member.mention}!")

    @commands.command(brief="Unban the user.", description="Unban's the user.")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member, *, reason = None):
        if not reason:
            reason = "Unspecified"
        user = await self.client.fetch_user(member)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'Unbanned {user.mention}.')
        return

    @commands.command(brief="Start a vote.", description="Start a vote.")
    @commands.has_permissions(manage_messages = True)
    async def start_vote(self, ctx, *, message):
        voteembed = discord.Embed(colour=discord.Colour.blue(), title=f"Vote started (by {ctx.author.display_name})", description=message)
        msg = await ctx.send(embed = voteembed)
        emoji = '\N{THUMBS UP SIGN}'
        emoji2 ='\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(emoji)
        await msg.add_reaction(emoji2)

    @commands.command(aliases=['purge', 'delete'], brief="Deletes messages.", description="Deletes messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Cleared {amount} messages.')

    @commands.command(aliases=['prefix', 'setprefix'], brief="Allows you to set prefix.", description="Allows you to set prefix.")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        prefix2 = f"SELECT prefix FROM prefixes WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(prefix2)
        myresult = mycursor.fetchall()
        if myresult:
            for x in myresult:
                y = str(x)[:-3][2:]
                await ctx.send(f"Prefix is already setted to `{y}` , use reset_prefix command to reset (then you can set again).")
                return
        else:
            sql = "INSERT INTO prefixes (prefix, serverid) VALUES (%s, %s)"
            val = (prefix, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setting prefix as `{prefix}`.')

    @commands.command(brief="Resets prefix.", description="Resets prefix.")
    @commands.has_permissions(administrator=True)
    async def reset_prefix(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        prefix2 = f"SELECT prefix FROM prefixes WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(prefix2)
        myresult = mycursor.fetchall()
        if myresult:
            prefix3 = f"DELETE FROM prefixes WHERE serverid ='{ctx.guild.id}'"
            mycursor.execute(prefix3)
            mydb.commit()
            await ctx.send('Resetted prefix.')
        else:
            await ctx.send('Prefix is not setted.')

    @commands.command(aliases=['welcome_ch', 'welcomech'], brief="Sets welcome channel.", description="Sets welcome channel as mentioned channel.")
    @commands.has_permissions(administrator=True)
    async def welcome_channel(self, ctx, channel : discord.TextChannel):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        chid = f"SELECT chid FROM welcomech WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(chid)
        myresult = mycursor.fetchall()
        if myresult:
            for x in myresult:
                y = str(x)[:-3][-18:]
                await ctx.send(f"Channel is already setted to <#{y}>, use reset_welcome_channel command to reset.")
                return
        else:
            sql = "INSERT INTO welcomech (chid, serverid) VALUES (%s, %s)"
            val = (channel.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setting new welcome channel as {channel.mention}.')

    @commands.command(aliases=['reset_welcomech'], brief="Resets welcome channel.", description="Resets welcome channel.")
    @commands.has_permissions(administrator=True)
    async def reset_welcome_channel(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        chid = f"SELECT chid FROM welcomech WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(chid)
        myresult = mycursor.fetchall()
        if myresult:
            await ctx.send('Resetting welcome_channel.')
            reset = f"DELETE FROM welcomech WHERE serverid ='{ctx.guild.id}'"
            mycursor.execute(reset)
            mydb.commit()
        else:
            await ctx.send('Welcome channel is not setted.')

    @commands.command(aliases=['reset_welcomemsg', 'reset_welcome_msg'], brief="Resets welcome message.", description="Resets welcome message.")
    @commands.has_permissions(administrator=True)
    async def reset_welcome_message(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        chid = f"SELECT msg FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(chid)
        myresult = mycursor.fetchall()
        if myresult:
            await ctx.send('Resetting welcome_message.')
            reset = f"DELETE FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
            mycursor.execute(reset)
            mydb.commit()
        else:
            await ctx.send('Welcome message is not setted.')

    @commands.command(aliases=['welcome_msg', 'welcomemsg'], brief="Sets new welcome message.", description="Sets new welcome message.(You can use {mention} for mention the user and {username} to see users username.)")
    @commands.has_permissions(administrator=True)
    async def welcome_message(self, ctx, *, message):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        msg = f"SELECT msg FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(msg)
        myresult = mycursor.fetchall()
        if myresult:
            await ctx.send('Message is already setted, use reset_welcome_message command to reset.')
            return
        else:
            msg2 = f"INSERT INTO welcomemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Setted new message.')

    @commands.command(aliases=['leavemsg', 'leave_msg'], brief="Sets new leave message.", description="Sets new leave message.(You can use {mention} for mention the user and {username} to see users username.)")
    @commands.has_permissions(administrator=True)
    async def leave_message(self, ctx, *, message):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="",
            database="sakuya" 
        )
        mycursor = mydb.cursor()
        msg = f"SELECT msg FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(msg)
        myresult = mycursor.fetchall()
        if myresult:
            await ctx.send('Message is already setted, use reset_leave_message command to reset.')
            return
        else:
            msg2 = f"INSERT INTO leavemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Setted new message.')

    @commands.command(brief="Resets leave message.", description="Resets leave message.", aliases=['reset_leavemsg', 'reset_leave_msg'])
    @commands.has_permissions(administrator=True)
    async def reset_leave_message(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        chid = f"SELECT msg FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(chid)
        myresult = mycursor.fetchall()
        if myresult:
            await ctx.send('Resetting leave_message.')
            reset = f"DELETE FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
            mycursor.execute(reset)
            mydb.commit()
        else:
            await ctx.send('Leave message is not setted.')

    @commands.command(brief="Sets leave channel.", description="Sets leave channel as mentioned channel.", aliases=['leave_ch', 'leavech'])
    @commands.has_permissions(administrator=True)
    async def leave_channel(self, ctx, channel : discord.TextChannel):
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
                y = str(x)[:-3][-18:]
                await ctx.send(f"Channel is already setted to <#{y}>, use reset_leave_channel command to reset.")
                return
        else:
            sql = "INSERT INTO leavech (chid, serverid) VALUES (%s, %s)"
            val = (channel.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setting new leave channel as {channel.mention}.')

    @commands.command(brief="Resets leave channel.", description="Resets leave channel.", aliases=['reset_leave_ch', 'reset_leavech', 'reset_leavechannel'])
    @commands.has_permissions(administrator=True)
    async def reset_leave_channel(self, ctx):
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
            await ctx.send('Resetting leave_channel.')
            reset = f"DELETE FROM leavech WHERE serverid ='{ctx.guild.id}'"
            mycursor.execute(reset)
            mydb.commit()
        else:
            await ctx.send('Leave channel is not setted.')

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

        embed = discord.Embed(colour=discord.Colour.red(), description=f"Settings of **{ctx.guild.name}**")
        embed.add_field(name="Leave channel", value=f"{leavechannel}")
        embed.add_field(name="Leave message", value=f"{leavemessage}")
        embed.add_field(name="Welcome channel", value=f"{welcomechannel}")
        embed.add_field(name="Welcome message", value=f"{welcomemessage}")
        embed.add_field(name="Autorole", value=f"{autorole2}")
        embed.add_field(name="Prefix", value=f"{prefix}")
        await ctx.send(embed=embed)

    @commands.command(brief="Allows you to set autorole", aliases=['auto_role'])
    @commands.has_permissions(administrator=True)
    async def autorole(self,ctx, role: discord.Role):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        role2 = f"SELECT roleid FROM autorole WHERE serverid ='{ctx.guild.id}'"
        mycursor.execute(role2)
        res = mycursor.fetchall()
        if res:
            await ctx.send('Auto role is already setted, use reset_autorole command to reset.')
            return
        else:
            sql = "INSERT INTO autorole (roleid, serverid) VALUES (%s, %s)"
            val = (role.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send('Successfully setted autorole.')

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
        afk2 = "INSERT INTO afk (isafk, memberid) VALUES (%s, %s)"
        value = ('true', ctx.author.id)
        cursor.execute(afk2, value)
        mydb.commit()
        embed2 = discord.Embed(colour=discord.Colour.blue(), description=f"{ctx.author.mention} you are now afk with reason: \n`{reason}`")
        await ctx.send(embed=embed2)

    @commands.command(brief="Warns user", description="Warns mentioned user")
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        cursor = mydb.cursor()
        warning = "INSERT INTO warns (memberid, warnreason, guildid) VALUES (%s, %s, %s)"
        values = (member.id, reason, ctx.guild.id)
        cursor.execute(warning, values)
        mydb.commit()
        await ctx.send(f'Warned {member.mention}')
        await member.send(f'You have been warned on **{ctx.guild.name}** \nWarn reason: {reason}')

def setup(client):
    client.add_cog(Moderation(client))
