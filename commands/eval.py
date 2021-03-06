import discord
from discord.ext import commands
import inspect

@commands.command(name='eval', pass_context=True, brief="Author command", description="Author command", hidden=True)
@commands.is_owner()
async def eval_(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await ctx.send(await res)
    else:
        await ctx.send(res)

def setup(client):
    client.add_command(eval_)
