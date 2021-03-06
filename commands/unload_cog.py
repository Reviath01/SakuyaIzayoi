import discord 
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def unload_cog(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded cogs.{extension}.')

def setup(client):
    client.add_command(unload_cog)
