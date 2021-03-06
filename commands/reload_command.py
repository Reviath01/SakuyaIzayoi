import discord
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def reload_command(ctx, command):
    client.unload_extension(f'commands.{extension}')
    client.load_extension(f'commands.{extension}')
    await ctx.send(f'Reloaded commands.{extension}.')

def setup(client):
    client.add_command(reload_command)
