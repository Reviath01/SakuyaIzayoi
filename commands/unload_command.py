import discord 
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def unload_command(ctx, extension):
    client.unload_extension(f'commands.{extension}')
    await ctx.send(f'Unloaded commands.{extension}.')

def setup(client):
    client.add_command(unload_command)
