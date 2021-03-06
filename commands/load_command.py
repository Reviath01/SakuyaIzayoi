import discord
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def load_command(ctx, extension):
    client.load_extension(f'commands.{extension}')
    await ctx.send(f'Loaded commands.{extension}.')

def setup(client):
    client.add_command(load_command)
