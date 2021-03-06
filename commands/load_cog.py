import discord
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def load_cog(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded cogs.{extension}.')

def setup(client):
    client.add_command(load_cog)
