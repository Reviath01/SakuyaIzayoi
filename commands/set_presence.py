import discord
from discord.ext import commands

@commands.command(brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def set_presence(ctx, *, presence):
    await ctx.send(f'Setting presence as "{presence}"')
    await client.change_presence(activity=discord.Game(presence))

def setup(client):
    client.add_command(set_presence)
