import discord
import os
from discord.ext import commands, tasks
import sys
import json
import inspect
import mysql.connector

intents = discord.Intents().all()
intents.members = True
intents.presences = True

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sakuya"
)

print(f"Successfully connected MySQL Database: \"{mydb.database}\"")

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents = intents)

@client.event
async def on_command_error(ctx, error):
    log = client.get_channel(790640302452375562)
    await ctx.send(error)
    await log.send(f'Error on server `{ctx.guild.name}` \n{error}')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_member_join(member):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sakuya"
    )
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
    else:
        return

@client.event
async def on_member_remove(member):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sakuya"
    )
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
            t = f"Goodbye {member.mention}"
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

@client.command(brief="Shows my code on gitlab", description="Shows my code on gitlab")
async def code(ctx):
    gitlabembed = discord.Embed(colour=ctx.author.top_role.colour, description="[Click here](https://git.randomchars.net/Reviath/sakuya-izayoi)")
    await ctx.send(embed=gitlabembed)

@client.command(brief="Shows my author", description="Shows my author")
async def author(ctx):
    authorembed = discord.Embed(description="My Author: \n<@!770218429096656917> ([Reviath#0001](https://discord.com/users/770218429096656917))", colour=discord.Colour.purple())
    await ctx.send(embed = authorembed)

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded cogs.{extension}.')

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded cogs.{extension}.')

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded cogs.{extension}.')

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shuting down!')
    await client.logout()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting...")
    log = client.get_channel(790640302452375562)
    await log.send('Restarting...')
    restart_program()

@client.command(brief="Author command", description="Author command")
@commands.is_owner()
async def set_presence(ctx, *, presence):
    await ctx.send(f'Setting presence as "{presence}"')
    await client.change_presence(activity=discord.Game(presence))

@client.command(name='eval', pass_context=True, brief="Author command", description="Author command")
@commands.is_owner()
async def eval_(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await ctx.send(await res)
    else:
        await ctx.send(res)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('TOKEN')
