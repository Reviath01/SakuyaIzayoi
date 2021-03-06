import discord
import os
from discord.ext import commands, tasks
import json
import mysql.connector
import datetime
import sys
import inspect

with open('config.json', 'r') as f:
    token_json = json.load(f)
    get_token = token_json['token']
    json_prefix = token_json['prefix']

intents = discord.Intents().all()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sakuya"
)

print(f"Successfully connected MySQL Database: \"{mydb.database}\"")

def get_prefix(client, message):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sakuya"
    )
    cursor = mydb.cursor()
    prefix = f"SELECT prefix FROM prefixes WHERE serverid='{message.guild.id}'"
    cursor.execute(prefix)
    res = cursor.fetchall()
    if res:
    	for x in res:
            y = str(x)[:-3][2:]
    else:
	    y = str(json_prefix)
        
    return commands.when_mentioned_or(y)(client, message)

client = commands.Bot(command_prefix = get_prefix, intents = intents, description=None, shard_count = 1)

@client.event
async def on_error(event, *args, **kwargs):
    await client.get_channel(790640302452375562).send(f"{event} {args} {kwargs}")

@client.event
async def on_member_update(before, after):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{before.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = before.guild.get_channel(int(y))

    if (before.display_name != after.display_name):
            embed1 = discord.Embed(colour=discord.Colour.red(), description=f"{before.mention}'s username updated!")
            embed1.add_field(name=f"User ID: \n{before.id}", value=f"Old name: `{before.display_name}` \nNew name: `{after.display_name}`")
            await logch.send(embed=embed1)
    
    if (before.roles != after.roles):
            embed2 = discord.Embed(colour=discord.Colour.blue(), description="User roles updated!")
            embed2.add_field(name=f"User", value=f"{before.mention} `({before.id})`")
            oldRoles = [role.mention for role in before.roles[1:]]
            oldRoles.append("@everyone")
            newRoles = [role.mention for role in after.roles[1:]]
            newRoles.append("@everyone")
            embed2.add_field(name="Old roles:", value=", ".join(oldRoles))
            embed2.add_field(name="New roles:", value=", ".join(newRoles))
            await logch.send(embed=embed2)

@client.event
async def on_guild_role_create(role):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{role.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = role.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Role created!", colour=role.colour)
    embed.add_field(name="Role name",value=f"{role.name} ({role.mention})", inline=False)
    embed.add_field(name="Role ID",value=role.id, inline=False)
    embed.add_field(name="Role color", value=role.colour, inline=False)
    await logch.send(embed=embed)

@client.event
async def on_guild_role_delete(role):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{role.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = role.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Role deleted!", colour=role.colour)
    embed.add_field(name="Role name",value=f"{role.name}", inline=False)
    embed.add_field(name="Role ID",value=role.id, inline=False)
    embed.add_field(name="Role color", value=role.colour, inline=False)
    await logch.send(embed=embed)

@client.event
async def on_guild_role_update(before, after):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{before.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = before.guild.get_channel(int(y))
    if before.name == after.name:
        if before.colour == after.colour:
            return
        else:
            embed = discord.Embed(description=f"Role updated!", colour=discord.Colour.purple())
            embed.add_field(name="Role name",value=f"{before.name} => {after.name}", inline=False)
            embed.add_field(name="Role",value=f"{before.mention} `({before.id})`", inline=False)
            embed.add_field(name="Role color", value=f"{before.colour} => {after.colour}", inline=False)
    else:
        embed = discord.Embed(description=f"Role updated!", colour=discord.Colour.purple())
        embed.add_field(name="Role name",value=f"{before.name} => {after.name}", inline=False)
        embed.add_field(name="Role",value=f"{before.mention} `({before.id})`", inline=False)
        embed.add_field(name="Role color", value=f"{before.colour} => {after.colour}", inline=False)
    await logch.send(embed=embed)

@client.event
async def on_guild_channel_update(before, after):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{before.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = before.guild.get_channel(int(y))
    if before.name != after.name:
        embed = discord.Embed(description=f"Channel updated!", colour=discord.Colour.red())
        embed.add_field(name="Channels old name:",value=before.name, inline=False)
        embed.add_field(name="Channels new name:",value=after.name, inline=False)
        embed.add_field(name="Type", value=before.type, inline=False)
        await logch.send(embed=embed)
    else:
        return

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{message.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    if not message.content:
        return
    logch = message.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Message sent by {message.author.mention} deleted!", colour=message.author.top_role.colour)
    embed.add_field(name="Message Content",value=message.content, inline=False)
    embed.add_field(name="Channel",value=f"{message.channel.mention} `({message.channel.name})`", inline=False)
    embed.add_field(name="User ID ", value=message.author.id, inline=False)
    await logch.send(embed=embed)


@client.event
async def on_guild_channel_delete(channel):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{channel.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = channel.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Channel deleted!", colour=discord.Colour.red())
    embed.add_field(name="Channel name",value=channel.name, inline=False)
    embed.add_field(name="Channel ID",value=channel.id, inline=False)
    embed.add_field(name="Type", value=channel.type, inline=False)
    await logch.send(embed=embed)

@client.event
async def on_guild_channel_create(channel):
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{channel.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    logch = channel.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Channel created!", colour=discord.Colour.red())
    embed.add_field(name="Channel name",value=f"{channel.name} ({channel.mention})", inline=False)
    embed.add_field(name="Channel ID",value=channel.id, inline=False)
    embed.add_field(name="Type", value=channel.type, inline=False)
    await logch.send(embed=embed)

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    cursor = mydb.cursor()
    ch = f"SELECT channelid FROM log WHERE guildid ='{before.guild.id}'"
    cursor.execute(ch)
    res = cursor.fetchall()
    if res:
        for x in res:
            y = str(x)[:-3][2:]
    else:
        return
    if not before.content:
        return
    if not after.content:
        return
    if after.content == before.content:
        return
    logch = before.guild.get_channel(int(y))
    embed = discord.Embed(description=f"Message sent by {before.author.mention} edited!", colour=before.author.top_role.colour)
    embed.add_field(name="Old",value=before.content, inline=False)
    embed.add_field(name="New", value=after.content, inline=False)
    embed.add_field(name="Channel",value=f"{before.channel.mention} `({before.channel.name})`", inline=False)
    embed.add_field(name="User ID", value=before.author.id, inline=False)
    await logch.send(embed=embed)

@client.event
async def on_message(message):
    cursor = mydb.cursor()
    settedprefix = f"SELECT prefix FROM prefixes WHERE serverid ='{message.guild.id}'"
    cursor.execute(settedprefix)
    ress = cursor.fetchall()
    if ress:
        for bb in ress:
            prefix = f"{str(bb)[:-3][2:]}"
    else:
        prefix = '!'

    if (message.content == f"<@!{client.user.id}>"):
        await message.channel.send(f"My prefix is {prefix}")

    isafk = f"SELECT isafk FROM afk WHERE memberid ='{message.author.id}' AND guildid ='{message.guild.id}'"
    cursor.execute(isafk)
    res = cursor.fetchall()
    if res:
        await message.channel.send(f'Welcome back {message.author.mention}')
        removeafk = f"DELETE FROM afk WHERE memberid ='{message.author.id}' AND guildid ='{message.guild.id}'"
        cursor.execute(removeafk)
        mydb.commit()
    afk2 = f"SELECT memberid FROM afk WHERE isafk ='true' AND guildid ='{message.guild.id}'"
    cursor.execute(afk2)
    res = cursor.fetchall()
    if res:
        for x in res:
            aaa = str(x)[:-3][2:]
        if aaa in message.content:
            if message.author == client.user:
                return
            await message.channel.send(f'This user is afk now!')
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    log = client.get_channel(790640302452375562)
    await ctx.send(error)
    await log.send(f'Error on server `{ctx.guild.name}` \n{error}')

@client.event
async def on_guild_join(guild):
    log = client.get_channel(790640302452375562)
    guildjoinembed = discord.Embed(colour=discord.Colour.blue(), description=(f"I am added to {guild.name}"))
    guildjoinembed.add_field(name="Guilds owner", value=f"{guild.owner.mention} `({guild.owner.display_name}, {guild.owner.id})`")
    guildjoinembed.add_field(name="Guilds member size", value=f"{guild.member_count}")
    guildjoinembed.set_thumbnail(url=f"{guild.icon_url}")
    await log.send(embed=guildjoinembed)

@client.event
async def on_guild_remove(guild):
        log = client.get_channel(790640302452375562)
        guildleaveembed = discord.Embed(colour=discord.Colour.blue(), description=(f"I have kicked from {guild.name}"))
        guildleaveembed.add_field(name="Guilds owner", value=f"{guild.owner.mention} `({guild.owner.display_name}, {guild.owner.id})`")
        guildleaveembed.add_field(name="Guilds member size", value=f"{guild.member_count}")
        guildleaveembed.set_thumbnail(url=f"{guild.icon_url}")
        await log.send(embed=guildleaveembed)

@client.event
async def on_member_join(member):
    mycursor = mydb.cursor()
    chid = f"SELECT chid FROM welcomech WHERE serverid ='{member.guild.id}'"
    mycursor.execute(chid)
    myresult = mycursor.fetchall()
    if myresult:
        msg = f"SELECT msg FROM welcomemsg WHERE serverid ='{member.guild.id}'"
        mycursor.execute(msg)
        myresult2 = mycursor.fetchall()
        if myresult2:
            for z in myresult2:
                t = str(z)[:-3][2:]
        else:
            t = f"Welcome to server {member.mention}"
        for x in myresult:
            y = str(x)[:-3][-18:]
            await member.guild.get_channel(int(y)).send(t.replace("{mention}", f"{member.mention}").replace("{username}", f"{member.display_name}").replace("{discriminator}", f"{member.discriminator}").replace("guild_name", f"{member.guild.name}"))

    cursor = mydb.cursor()
    getrole = f"SELECT roleid FROM autorole WHERE serverid ='{member.guild.id}'"
    cursor.execute(getrole)
    res = cursor.fetchall()
    if res:
        for a in res:
            b = str(a)[:-3][2:]
            role2 = discord.utils.get(member.guild.roles, id=int(b))
            await member.add_roles(role2)

@client.event
async def on_member_remove(member):
    mycursor = mydb.cursor()
    chid = f"SELECT chid FROM leavech WHERE serverid ='{member.guild.id}'"
    mycursor.execute(chid)
    myresult = mycursor.fetchall()
    if myresult:
        msg = f"SELECT msg FROM leavemsg WHERE serverid ='{member.guild.id}'"
        mycursor.execute(msg)
        myresult2 = mycursor.fetchall()
        if myresult2:
            for z in myresult2:
                t = str(z)[:-3][2:]
        else:
            t = f"{member.mention} left the server."
        for x in myresult:
            y = str(x)[:-3][-18:]
            await member.guild.get_channel(int(y)).send(t.replace("{mention}", f"{member.mention}").replace("{username}", f"{member.display_name}").replace("{discriminator}", f"{member.discriminator}").replace("guild_name", f"{member.guild.name}"))
    else:
        return

@client.event
async def on_ready():
    log = client.get_channel(790640302452375562)
    await client.change_presence(activity=discord.Game("Prefix: !"))
    print(client.user.display_name + '#' + client.user.discriminator + ' is ready!')
    await log.send('I am ready to use!')

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def load_cog(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded cogs.{extension}.')

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def unload_cog(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded cogs.{extension}.')

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def reload_cog(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded cogs.{extension}.')

@client.command(brief="Shows my author", description="Shows my author")
async def author(ctx):
    authorembed = discord.Embed(description="My Author: \n<@!770218429096656917> ([Reviath#0001](https://discord.com/users/770218429096656917))", colour=discord.Colour.purple())
    await ctx.send(embed = authorembed)

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shuting down!')
    await client.logout()

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def set_presence(ctx, *, presence):
    await ctx.send(f'Setting presence as "{presence}"')
    await client.change_presence(activity=discord.Game(presence))

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting...")
    restart_program()

@client.command(name='eval', pass_context=True, brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def eval_(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await ctx.send(await res)
    else:
        await ctx.send(res)

@client.command(brief="Allows you to create issue", description="Allows you to create issue")
async def issue(ctx):
    issueembed = discord.Embed(colour=ctx.author.top_role.colour, description="[Click here to create issue on GitLab](https://git.randomchars.net/Reviath/sakuya-izayoi) \n[If you don't know how to use GitLab, you can come to our server and specify the problem.](https://discord.gg/xqsTvtM2hk)")
    await ctx.send(embed=issueembed)

@client.command(brief="Sends vote link.", description="Sends vote link.")
async def vote(ctx):
    await ctx.send(embed=discord.Embed(colour=ctx.author.top_role.colour, description=f"[Click here!](https://top.gg/bot/{client.user.id}/vote) \nAlso if you vote, you will get a role in my [guild](https://discord.gg/Nvte7RYfqY)"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded cogs.{filename[:-3]}.")

client.run(str(get_token))
