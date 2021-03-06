import discord
from discord.ext import commands

@commands.command(brief="Shows my author", description="Shows my author")
async def author(ctx):
    authorembed = discord.Embed(description="My Author: \n<@!770218429096656917> ([Reviath#0001](https://discord.com/users/770218429096656917))", colour=discord.Colour.purple())
    await ctx.send(embed = authorembed)

def setup(client):
    client.add_command(author)
