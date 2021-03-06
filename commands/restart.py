import discord
from discord.ext import commands
import sys

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting...")
    log = client.get_channel(790640302452375562)
    await log.send('Restarting...')
    restart_program()

def setup(client):
    client.add_command(restart)
