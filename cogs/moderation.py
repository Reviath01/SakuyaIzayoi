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
        if amount < 1:
            await ctx.send('Amount must be greater than 1')
            return
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Cleared {amount} messages.', delete_after=5)

    @commands.command(aliases=['prefix', 'setprefix'], brief="Allows you to set prefix.", description="Allows you to set prefix.")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix = None):
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
            if prefix == None:
                dlt = f"DELETE FROM prefixes WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                await ctx.send('Resetted prefix.')
            else:
                dlt = f"DELETE FROM prefixes WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                sql = "INSERT INTO prefixes (prefix, serverid) VALUES (%s, %s)"
                val = (prefix, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send(f'Setted new prefix as {prefix}.')                
        else:
            if prefix == None:
                await ctx.send('You need to specify new prefix.')
                return
            sql = "INSERT INTO prefixes (prefix, serverid) VALUES (%s, %s)"
            val = (prefix, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setted prefix as {prefix}.')

    @commands.command(aliases=['welcome_ch', 'welcomech'], brief="Sets welcome channel.", description="Sets welcome channel as mentioned channel.")
    @commands.has_permissions(administrator=True)
    async def welcome_channel(self, ctx, channel : discord.TextChannel = None):
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
            if channel == None:
                dlt = f"DELETE FROM welcomech WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                await ctx.send('Resetted welcome.channel.')
            else:
                dlt = f"DELETE FROM welcomech WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                sql = "INSERT INTO welcomech (chid, serverid) VALUES (%s, %s)"
                val = (channel.id, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send(f'Setted new welcome.channel as {channel.mention}.')
                
        else:
            sql = "INSERT INTO welcomech (chid, serverid) VALUES (%s, %s)"
            val = (channel.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setting welcome channel as {channel.mention}.')

    @commands.command(aliases=['welcome_msg', 'welcomemsg'], brief="Sets new welcome message.", description="Sets new welcome message.(You can use {mention} for mention the user and {username} to see users username.)")
    @commands.has_permissions(administrator=True)
    async def welcome_message(self, ctx, *, message = None):
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
            if message == None:
                msg3 = f"DELETE FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(msg3)
                mydb.commit()
                await ctx.send('Resetted welcome.message.')
            else:
                msg4 = f"DELETE FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(msg4)
                mydb.commit()
                msg2 = "INSERT INTO welcomemsg (msg, serverid) VALUES (%s, %s)"
                val = (message, ctx.guild.id)
                mycursor.execute(msg2, val)
                mydb.commit()
                await ctx.send('Setted new welcome.message.')
        else:
            msg2 = "INSERT INTO welcomemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Setted welcome.message.')

    @commands.command(aliases=['leavemsg', 'leave_msg'], brief="Sets new leave message.", description="Sets new leave message.(You can use {mention} for mention the user and {username} to see users username.)")
    @commands.has_permissions(administrator=True)
    async def leave_message(self, ctx, *, message = None):
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
            if message == None:
                dlt = f"DELETE FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                await ctx.send('Resetted leave.message.')
            else:
                dlt = f"DELETE FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                msg2 = "INSERT INTO leavemsg (msg, serverid) VALUES (%s, %s)"
                val = (message, ctx.guild.id)
                mycursor.execute(msg2, val)
                mydb.commit()
                await ctx.send(f'Setted new leave.message.')
        else:
            msg2 = "INSERT INTO leavemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Setted leave.message.')

    @commands.command(brief="Sets leave channel.", description="Sets leave channel as mentioned channel.", aliases=['leave_ch', 'leavech'])
    @commands.has_permissions(administrator=True)
    async def leave_channel(self, ctx, channel : discord.TextChannel = None):
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
            if channel == None:
                dltch = f"DELETE FROM leavech WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dltch)
                mydb.commit()
                await ctx.send('Resetted leave channel')
            else:
                delch = f"DELETE FROM leavech WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(delch)
                mydb.commit()
                sql = "INSERT INTO leavech (chid, serverid) VALUES (%s, %s)"
                val = (channel.id, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send(f'Setting new leave channel as {channel.mention}.')
        else:
            sql = "INSERT INTO leavech (chid, serverid) VALUES (%s, %s)"
            val = (channel.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Setting leave channel as {channel.mention}.')

    @commands.command(brief="Allows you to set autorole", aliases=['auto_role'])
    @commands.has_permissions(administrator=True)
    async def autorole(self,ctx, role: discord.Role = None):
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
            if role == None:
                sql2 = f"DELETE FROM autorole WHERE serverid = '{ctx.guild.id}'"
                mycursor.execute(sql2)
                mydb.commit()
                await ctx.send('Resetted autorole.')
            else:
                sql2 = f"DELETE FROM autorole WHERE serverid = '{ctx.guild.id}'"
                mycursor.execute(sql2)
                mydb.commit()
                sql = "INSERT INTO autorole (roleid, serverid) VALUES (%s, %s)"
                val = (role.id, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send('Successfully setted new autorole.')
        else:
            sql = "INSERT INTO autorole (roleid, serverid) VALUES (%s, %s)"
            val = (role.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send('Successfully setted autorole.')

    @commands.command(brief="Warns user.", description="Warns mentioned user.")
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

    @commands.command(brief="Allows you to delete all warns for user.", description="Allows you to delete all warns for user.")
    @commands.has_permissions(administrator=True)
    async def delete_warns(self, ctx, member : discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        cursor = mydb.cursor()
        deletewarns = f"DELETE FROM warns WHERE memberid ='{member.id}' AND guildid ='{ctx.guild.id}'"
        cursor.execute(deletewarns)
        mydb.commit()
        await ctx.send(f'Deleted all warns for specified user.')

    @commands.command(brief="Deletes all warns on your guild.", description="Deletes all warns on your guild.")
    @commands.has_permissions(administrator=True)
    async def delete_all_warns(self, ctx):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        cursor = mydb.cursor()
        allwarns = f"DELETE FROM warns WHERE guildid ='{ctx.guild.id}'"
        cursor.execute(allwarns)
        mydb.commit()
        await ctx.send('All warns have been resetted.')

    @commands.command(brief="Sets logging channel", description="Sets logging channel as mentioned channel, if you don't mention a channel it will be reset")
    @commands.has_permissions(administrator=True)
    async def log(self, ctx, channel : discord.TextChannel = None):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        cursor = mydb.cursor()
        ifch = f"SELECT channelid FROM log WHERE guildid ='{ctx.guild.id}'"
        cursor.execute(ifch)
        res = cursor.fetchall()
        if res: 
            if channel == None:
                delch = f"DELETE FROM log WHERE guildid ='{ctx.guild.id}'"
                cursor.execute(delch)
                mydb.commit()
                await ctx.send('Resetted log')
            else:
                delch = f"DELETE FROM log WHERE guildid ='{ctx.guild.id}'"
                cursor.execute(delch)
                mydb.commit()
                setch = "INSERT INTO log (channelid, guildid) VALUES (%s, %s)"
                val = (channel.id, ctx.guild.id)
                cursor.execute(setch, val)
                mydb.commit()
                await ctx.send(f'Setting new log as {channel.mention}')
            return
        setch = "INSERT INTO log (channelid, guildid) VALUES (%s, %s)"
        val = (channel.id, ctx.guild.id)
        cursor.execute(setch, val)
        mydb.commit()
        await ctx.send(f'Setted log channel as {channel.mention}')

def setup(client):
    client.add_cog(Moderation(client))
