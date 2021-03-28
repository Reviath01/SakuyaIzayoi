import discord
from discord.ext import commands
import json
import mysql.connector

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Ban the user.", description="Allow's you to ban the user.")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.User, *, reason = None):
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
                if y == "ban":
                    await ctx.send('This command is disabled on this guild.')
                    return
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
                if y == "kick":
                    await ctx.send('This command is disabled on this guild.')
                    return
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
                if y == "unban":
                    await ctx.send('This command is disabled on this guild.')
                    return
        if not reason:
            reason = "Unspecified"
        user = await self.client.fetch_user(member)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'Unbanned {user.mention}.')
        return

    @commands.command(brief="Start a vote.", description="Start a vote.")
    @commands.has_permissions(manage_messages = True)
    async def start_vote(self, ctx, *, message):
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
                if y == "start_vote":
                    await ctx.send('This command is disabled on this guild.')
                    return
        voteembed = discord.Embed(colour=discord.Colour.blue(), title=f"Vote started (by {ctx.author.display_name})", description=message)
        msg = await ctx.send(embed = voteembed)
        emoji = '\N{THUMBS UP SIGN}'
        emoji2 ='\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(emoji)
        await msg.add_reaction(emoji2)

    @commands.command(aliases=['purge', 'delete'], brief="Deletes messages.", description="Deletes messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
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
                if y == "clear":
                    await ctx.send('This command is disabled on this guild.')
                    return
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
                await ctx.send('Reset prefix.')
            else:
                dlt = f"DELETE FROM prefixes WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                sql = "INSERT INTO prefixes (prefix, serverid) VALUES (%s, %s)"
                val = (prefix, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send(f'Set new prefix as {prefix}.')
        else:
            if prefix == None:
                await ctx.send('You need to specify new prefix.')
                return
            sql = "INSERT INTO prefixes (prefix, serverid) VALUES (%s, %s)"
            val = (prefix, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send(f'Set prefix as {prefix}.')

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
                await ctx.send('Reset welcome.channel.')
            else:
                dlt = f"DELETE FROM welcomech WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                sql = "INSERT INTO welcomech (chid, serverid) VALUES (%s, %s)"
                val = (channel.id, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send(f'Set new welcome.channel as {channel.mention}.')
        else:
            if channel == None:
                await ctx.send("You need to specify the channel.")
                return
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
                await ctx.send('Reset welcome.message.')
            else:
                msg4 = f"DELETE FROM welcomemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(msg4)
                mydb.commit()
                msg2 = "INSERT INTO welcomemsg (msg, serverid) VALUES (%s, %s)"
                val = (message, ctx.guild.id)
                mycursor.execute(msg2, val)
                mydb.commit()
                await ctx.send('Set new welcome.message.')
        else:
            msg2 = "INSERT INTO welcomemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Set welcome.message.')

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
                await ctx.send('Reset leave.message.')
            else:
                dlt = f"DELETE FROM leavemsg WHERE serverid ='{ctx.guild.id}'"
                mycursor.execute(dlt)
                mydb.commit()
                msg2 = "INSERT INTO leavemsg (msg, serverid) VALUES (%s, %s)"
                val = (message, ctx.guild.id)
                mycursor.execute(msg2, val)
                mydb.commit()
                await ctx.send(f'Set new leave.message.')
        else:
            msg2 = "INSERT INTO leavemsg (msg, serverid) VALUES (%s, %s)"
            val = (message, ctx.guild.id)
            mycursor.execute(msg2, val)
            mydb.commit()
            await ctx.send('Set leave.message.')

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
                await ctx.send('Reset leave channel')
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
            if channel == None:
                await ctx.send("You need to specify the channel.")
                return
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
                await ctx.send('Reset autorole.')
            else:
                sql2 = f"DELETE FROM autorole WHERE serverid = '{ctx.guild.id}'"
                mycursor.execute(sql2)
                mydb.commit()
                sql = "INSERT INTO autorole (roleid, serverid) VALUES (%s, %s)"
                val = (role.id, ctx.guild.id)
                mycursor.execute(sql, val)
                mydb.commit()
                await ctx.send('Successfully set new autorole.')
        else:
            sql = "INSERT INTO autorole (roleid, serverid) VALUES (%s, %s)"
            val = (role.id, ctx.guild.id)
            mycursor.execute(sql, val)
            mydb.commit()
            await ctx.send('Successfully set autorole.')

    @commands.command(brief="Warns user.", description="Warns mentioned user.")
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
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
                if y == "warn":
                    await ctx.send('This command is disabled on this guild.')
                    return
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
        await ctx.send('All warns have been reset.')

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
                await ctx.send('Reset log.')
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
        await ctx.send(f'Set log channel as {channel.mention}')

    @commands.command(brief="Allows you to disable command", description="Allows you to disable command")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, command):
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
            for z in res:
                t = str(z)[:-3][2:]
            if t == command:
                await ctx.send('This command is already disabled.')
                return
        else:
            sql2 = "INSERT INTO disabledcommands (commandname, guildid) VALUES (%s, %s)"
            val = (command, ctx.guild.id)
            mycursor.execute(sql2, val)
            mydb.commit()
            await ctx.send(f'Disabled {command}.')

    @commands.command(brief="Allows you to enable command", description="Allows you to enable command")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, command):
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
            for z in res:
                t = str(z)[:-3][2:]
            if t != command:
                await ctx.send(f'This command is already enabled or I can\'t find command {command}.')
                return
            sql2 = f"DELETE FROM disabledcommands WHERE commandname ='{command}' AND guildid ='{ctx.guild.id}'"
            mycursor.execute(sql2)
            mydb.commit()
            await ctx.send(f'Enabled {command}.')
        else:
            await ctx.send('There is no disabled commands on this guild')

    @commands.command(brief="Allows you to set muted role", description="Allows you to set muted role")
    @commands.has_permissions(administrator=True)
    async def muted_role(self, ctx, role: discord.Role = None):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT role FROM mutedroles WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            if role == None:
                sql2 = f"DELETE FROM mutedroles WHERE guildid ='{ctx.guild.id}'"
                mycursor.execute(sql2)
                mydb.commit()
                await ctx.send('Reset muted role.')
                return
            else:
                sql3 = f"DELETE FROM mutedroles WHERE guildid ='{ctx.guild.id}'"
                mycursor.execute(sql3)
                mydb.commit()
                sql4 = f"INSERT INTO mutedroles (role, guildid) VALUES ({role.id}, {ctx.guild.id})"
                mycursor.execute(sql4)
                await ctx.send('Set new muted role.')
                mydb.commit()
                return
        if role == None:
            await ctx.send('You need to mention a role.')
            return
        else:
            sql5 = f"INSERT INTO mutedroles (role, guildid) VALUES ({role.id}, {ctx.guild.id})"
            mycursor.execute(sql5)
            mydb.commit()
            await ctx.send('Set muted role.')

    @commands.command(brief="Allows you to mute someone.", description="Gives muted role to user.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT role FROM mutedroles WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
            role3 = discord.utils.get(ctx.guild.roles, id=int(y))
            for x in user.roles:
                if x == role3:
                    await ctx.send('This user is already muted.')
                    return
            await user.add_roles(role3)
            await ctx.send(f'Muted {user.mention}.')
        else:
            await ctx.send('Muted role is not set (Use !muted_role command to set).')

    @commands.command(brief="Allows you to unmute someone.", description="Removes muted role from user.")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sakuya"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT role FROM mutedroles WHERE guildid ='{ctx.guild.id}'"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        if res:
            for x in res:
                y = str(x)[:-3][2:]
            mutedrole2 = discord.utils.get(ctx.guild.roles, id=int(y))
            for mutedrole3 in user.roles:
                if mutedrole3 == mutedrole2:
                    await user.remove_roles(mutedrole3)
                    await ctx.send('Unmuted user.')
                    return
            await ctx.send('This user is not muted.')
        else:
            await ctx.send('Muted role is not set (Use muted_role command to set).')

def setup(client):
    client.add_cog(Moderation(client))
