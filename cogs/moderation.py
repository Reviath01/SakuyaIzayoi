import discord
from discord.ext import commands
import json
import mysql.connector

intents = discord.Intents()

intents.members = True

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation commands are loaded!')

    @commands.command(brief="Ban the user.", description="Allow's you to ban the user.")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.User = None, reason = None):
        if member == None:
            await ctx.send('You need to mention someone.')
            return
        if member == ctx.message.author:
            await ctx.send('You can\'t ban yourself.')
            return
        if reason == None:
            reason = "Unspecified"
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"Banned {member}!")

    @commands.command(brief="Kick the user.", description="Allow's you to kick the user.")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.User = None, reason = None):
        if member == None:
            await ctx.send('You need to mention someone.')
            return
        if member == ctx.message.author:
            await ctx.send('You can\'t kick yourself.')
            return
        if reason == None:
            reason = "Unspecified"
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"Kicked {member}!")

    @commands.command(brief="Unban the user.", description="Unban's the user.")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member = None):
        if member == None:
            await ctx.send('You need to specify a ID.')
            return
        user = await self.client.fetch_user(member)
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned <@{user.id}>.')
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

    @commands.command(brief="Deletes messages.", description="Deletes messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Cleared {amount} messages.')

    @commands.command(brief="Allows you to set prefix.", description="Allows you to set prefix.")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix=None):
        if prefix == None:
            await ctx.send('You need to send new prefix.')
            return
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send('Succesfully changed prefix.')

    @commands.command(brief="Sets welcome channel.", description="Sets welcome channel as mentioned channel.")
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

    @commands.command(brief="Resets welcome channel.", description="Resets welcome channel.")
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

    @commands.command(brief="Resets welcome message.", description="Resets welcome message.")
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

    @commands.command(brief="Sets new welcome message.", description="Sets new welcome message.(You can use {mention} for mention the user and {username} to see users username.)")
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

    @commands.command(brief="Sets new leave message.", description="Sets new leave message.(You can use {mention} for mention the user and {username} to see users username.)")
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

    @commands.command(brief="Resets leave message.", description="Resets leave message.")
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

    @commands.command(brief="Sets leave channel.", description="Sets leave channel as mentioned channel.")
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

    @commands.command(brief="Resets leave channel.", description="Resets leave channel.")
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

def setup(client):
    client.add_cog(Moderation(client))
