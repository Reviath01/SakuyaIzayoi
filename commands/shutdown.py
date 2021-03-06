import discord
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shuting down!')
    await client.logout()

def setup(client):
    client.add_command(shutdown)
